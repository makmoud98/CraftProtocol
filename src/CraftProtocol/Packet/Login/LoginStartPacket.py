#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class LoginStartPacket(BasePacket):

	PACKET_ID = 0x00
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, username):
		BasePacket.__init__(self)
		self.username = username

	def get_username(self):
		return self.username

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.username.encode("utf8"))

	@staticmethod
	def read(stream, packet_size):
		username = StreamIO.read_string(stream).decode("utf8")

		return LoginStartPacket(username)