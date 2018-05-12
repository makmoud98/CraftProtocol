#!/usr/bin/env python

import json
from CraftPlayer import CraftPlayer
from KickError import KickError
from ..ProtocolState import ProtocolState
from ..ProtocolVersion import ProtocolVersion
from ..ChatSerializer import ChatSerializer
from ..Packet import *
import socket

class CraftServer(object):

	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port
		self.protocol = ProtocolVersion.MC_1_10 # currently only supported protocol version

	def ping(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)

		sock.connect((self.hostname, self.port))

		serializer = PacketSerializer(PacketDirection.SERVERBOUND)

		handshake = Handshaking.HandshakePacket(self.protocol, self.hostname, self.port, ProtocolState.STATUS)
		request = Status.RequestPacket()

		serializer.write(sock, handshake)
		serializer.set_state(ProtocolState.STATUS)
		serializer.write(sock, request)

		response = serializer.read(sock)
		if not isinstance(response, Status.ResponsePacket):
			return None

		response = json.loads(response.get_json())

		sock.close()
		return response

	def login(self, username):
		if len(username) > 16:
			raise IOError("Username is too long")

		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(10)

			sock.connect((self.hostname, self.port))

			serializer = PacketSerializer(PacketDirection.SERVERBOUND)

			handshake = Handshaking.HandshakePacket(self.protocol, self.hostname, self.port, ProtocolState.LOGIN)
			login = Login.LoginStartPacket(username)

			serializer.write(sock, handshake)
			serializer.set_state(ProtocolState.LOGIN)
			serializer.write(sock, login)

			response = serializer.read(sock)
			while not isinstance(response, Login.LoginSuccessPacket):
				if isinstance(response, Login.DisconnectPacket):
					raise KickError(ChatSerializer.strip_colors(json.loads(response.get_reason())))
				elif isinstance(response, Login.SetCompressionPacket):
					serializer.set_threshold(response.get_threshold())
				elif isinstance(response, Login.EncryptionRequestPacket):
					sock.close()
					raise KickError("Encryption is currently not supported")

				response = serializer.read(sock)

			serializer.set_state(ProtocolState.PLAY)
			return CraftPlayer(response.get_username(), response.get_uuid(), sock, serializer, self)
		except socket.timeout:
			raise KickError("Timed out")
		except socket.error as ex:
			raise KickError(str(ex))