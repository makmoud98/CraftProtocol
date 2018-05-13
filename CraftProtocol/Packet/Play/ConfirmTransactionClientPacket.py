#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class ConfirmTransactionClientPacket(BasePacket):

	PACKET_ID = 0x11
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, window_id, action, accepted):
		BasePacket.__init__(self)
		self.window_id = window_id
		self.action = action
		self.accepted = accepted

	def get_window_id(self):
		return self.window_id

	def get_action(self):
		return self.action

	def is_accepted(self):
		return self.accepted

	@staticmethod
	def write(stream, packet):
		StreamIO.write_byte(stream, packet.window_id)
		StreamIO.write_short(stream, packet.action)
		StreamIO.write_bool(stream, packet.accepted)

	@staticmethod
	def read(stream, packet_size):
		window_id = StreamIO.read_byte(stream)
		action = StreamIO.read_short(stream)
		accepted = StreamIO.read_bool(stream)

		return ConfirmTransactionClientPacket(window_id, action, accepted)