#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class ClientStatusPacket(BasePacket):

	class ClientStatus(object):

		PERFORM_RESPAWN = 0
		REQUEST_STATS = 1
		OPEN_INVENTORY = 2

	PACKET_ID = 0x03
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, action):
		BasePacket.__init__(self)
		self.action = action

	def get_action(self):
		return self.action

	@staticmethod
	def write(stream, packet):
		StreamIO.write_varint(stream, packet.action)

	@staticmethod
	def read(stream, packet_size):	
		action = StreamIO.read_varint(stream)

		return ClientStatusPacket(action)