#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class KeepAliveClientPacket(BasePacket):

	PACKET_ID = 0x1F
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, id):
		BasePacket.__init__(self)
		self.id = id

	def get_id(self):
		return self.id

	@staticmethod
	def write(stream, packet):
		StreamIO.write_varint(stream, packet.id)

	@staticmethod
	def read(stream, packet_size):	
		id = StreamIO.read_varint(stream)

		return KeepAliveClientPacket(id)