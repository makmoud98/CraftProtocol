#!/usr/bin/env python

from BaseEvent import BaseEvent

class PacketOutEvent(BaseEvent):

	def __init__(self, packet):
		BaseEvent.__init__(self)
		self.packet = packet

	def get_packet(self):
		return self.packet

	def set_packet(self, packet):
		self.packet = packet