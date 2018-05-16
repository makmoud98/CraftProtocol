#!/usr/bin/env python

import json
import socket

from CraftPlayer import CraftPlayer
from KickError import KickError
from PingError import PingError
from ..ChatSerializer import ChatSerializer
from ..Packet import *
from ..ProtocolState import ProtocolState


class CraftServer(object):

    def __init__(self, hostname, port, protocol):
        self._hostname = hostname
        self._port = port
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def ping(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)

            sock.connect((self._hostname, self._port))
            serializer = PacketSerializer(PacketDirection.SERVERBOUND)

            serializer.write(sock,
                         Handshaking.HandshakePacket(self._protocol, self._hostname, self._port, ProtocolState.STATUS))
            serializer.set_state(ProtocolState.STATUS)
            serializer.write(sock, Status.RequestPacket())

            response = serializer.read(sock)
            if not isinstance(response, Status.ResponsePacket):
                return None

            response = json.loads(response.get_json())
            sock.close()

            return response
        except:
            raise PingError()

    def login(self, username):
        if len(username) > 16:
            raise IOError("Username is too long")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)

            sock.connect((self._hostname, self._port))
            serializer = PacketSerializer(PacketDirection.SERVERBOUND)

            serializer.write(sock, Handshaking.HandshakePacket(self._protocol, self._hostname, self._port,
                                                               ProtocolState.LOGIN))
            serializer.set_state(ProtocolState.LOGIN)
            serializer.write(sock, Login.LoginStartPacket(username))

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
        except EOFError as ex:
            raise KickError(str(ex))
