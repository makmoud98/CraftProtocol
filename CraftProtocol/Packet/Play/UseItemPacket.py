#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class UseItemPacket(BasePacket):

	PACKET_ID = 0x1D
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, hand):
		BasePacket.__init__(self)
		self.hand = hand

	def get_hand(self):
		return self.hand

	@staticmethod
	def write(stream, packet):
		StreamIO.write_varint(stream, packet.hand)

	@staticmethod
	def read(stream, packet_size):	
		hand = StreamIO.read_varint(stream)

		return UseItemPacket(hand)