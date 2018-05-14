#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class TeleportConfirmPacket(BasePacket):

	PACKET_ID = 0x00
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, teleport_id):
		BasePacket.__init__(self)
		self._teleport_id = teleport_id

	def get_teleport_id(self):
		return self._teleport_id

	@staticmethod
	def write(stream, packet):
		StreamIO.write_varint(stream, packet._teleport_id)

	@staticmethod
	def read(stream, packet_size):	
		teleport_id = StreamIO.read_varint(stream)

		return TeleportConfirmPacket(teleport_id)