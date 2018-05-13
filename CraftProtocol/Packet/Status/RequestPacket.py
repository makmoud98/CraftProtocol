#!/usr/bin/env python

from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class RequestPacket(BasePacket):

	PACKET_ID = 0x00
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self):
		BasePacket.__init__(self)

	@staticmethod
	def write(stream, packet):
		pass

	@staticmethod
	def read(stream, packet_size):
		return RequestPacket()