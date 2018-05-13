#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class CloseWindowServerPacket(BasePacket):

	PACKET_ID = 0x08
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

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

		return CloseWindowServerPacket(window_id)