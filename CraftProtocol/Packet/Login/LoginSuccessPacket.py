#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class LoginSuccessPacket(BasePacket):

	PACKET_ID = 0x02
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, uuid, username):
		BasePacket.__init__(self)
		self.uuid = uuid
		self.username = username

	def get_uuid(self):
		return self.uuid

	def get_username(self):
		return self.username

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.uuid.encode("utf8"))
		StreamIO.write_string(stream, packet.username.encode("utf8"))

	@staticmethod
	def read(stream, packet_size):
		uuid = StreamIO.read_string(stream).decode("utf8")
		username = StreamIO.read_string(stream).decode("utf8")

		return LoginSuccessPacket(uuid, username)