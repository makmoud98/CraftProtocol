#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class CloseWindowClientPacket(BasePacket):

	PACKET_ID = 0x12
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, window_id):
		BasePacket.__init__(self)
		self.window_id = window_id

	def get_window_id(self):
		return self.window_id

	@staticmethod
	def write(stream, packet):
		StreamIO.write_ubyte(stream, packet.window_id)

	@staticmethod
	def read(stream, packet_size):	
		window_id = StreamIO.read_ubyte(stream)

		return CloseWindowClientPacket(window_id)