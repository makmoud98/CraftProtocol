#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class PlayerPositionAndLookClientPacket(BasePacket):

	PACKET_ID = 0x2E
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, x, y, z, yaw, pitch, flags, teleport_id):
		BasePacket.__init__(self)
		self.x = x
		self.y = y
		self.z = z
		self.yaw = yaw
		self.pitch = pitch
		self.flags = flags
		self.teleport_id = teleport_id

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_z(self):
		return self.z

	def get_yaw(self):
		return self.yaw

	def get_pitch(self):
		return self.pitch

	def get_flags(self):
		return self.flags

	def get_teleport_id(self):
		return self.teleport_id

	@staticmethod
	def write(stream, packet):
		StreamIO.write_double(stream, packet.x)
		StreamIO.write_double(stream, packet.y)
		StreamIO.write_double(stream, packet.z)
		StreamIO.write_float(stream, packet.yaw)
		StreamIO.write_float(stream, packet.pitch)
		StreamIO.write_byte(stream, packet.flags)
		StreamIO.write_varint(stream, packet.teleport_id)

	@staticmethod
	def read(stream, packet_size):
		x = StreamIO.read_double(stream)
		y = StreamIO.read_double(stream)
		z = StreamIO.read_double(stream)
		yaw = StreamIO.read_float(stream)
		pitch = StreamIO.read_float(stream)
		flags = StreamIO.read_byte(stream)
		teleport_id = StreamIO.read_varint(stream)

		return PlayerPositionAndLookClientPacket(x, y, z, yaw, pitch, flags, teleport_id)