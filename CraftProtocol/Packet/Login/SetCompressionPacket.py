#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class SetCompressionPacket(BasePacket):

	PACKET_ID = 0x03
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, threshold):
		BasePacket.__init__(self)
		self.threshold = threshold

	def get_threshold(self):
		return self.threshold

	@staticmethod
	def write(stream, packet):
		StreamIO.write_varint(stream, packet.threshold)

	@staticmethod
	def read(stream, packet_size):
		threshold = StreamIO.read_varint(stream)

		return SetCompressionPacket(threshold)