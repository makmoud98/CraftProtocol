#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class PlayerPositionServerPacket(BasePacket):

	PACKET_ID = 0x0C
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, x, y, z, on_ground):
		BasePacket.__init__(self)
		self.x = x
		self.y = y
		self.z = z
		self.on_ground = on_ground

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_z(self):
		return self.z

	def is_on_ground(self):
		return self.on_ground

	@staticmethod
	def write(stream, packet):
		StreamIO.write_double(stream, packet.x)
		StreamIO.write_double(stream, packet.y)
		StreamIO.write_double(stream, packet.z)
		StreamIO.write_bool(stream, packet.on_ground)

	@staticmethod
	def read(stream, packet_size):
		x = StreamIO.read_double(stream)
		y = StreamIO.read_double(stream)
		z = StreamIO.read_double(stream)
		on_ground = StreamIO.read_bool(stream)

		return PlayerPositionServerPacket(x, y, z, on_ground)