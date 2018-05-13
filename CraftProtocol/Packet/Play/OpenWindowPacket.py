#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class OpenWindowPacket(BasePacket):

	PACKET_ID = 0x13
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, window_id, window_type, window_title, slots_number, entity_id):
		BasePacket.__init__(self)
		self.window_id = window_id
		self.window_type = window_type
		self.window_title = window_title
		self.slots_number = slots_number
		self.entity_id = entity_id

	def get_window_id(self):
		return self.window_id

	def get_window_type(self):
		return self.window_type

	def get_window_title(self):
		return self.window_title

	def get_slots_number(self):
		return self.slots_number

	def get_entity_id(self):
		return self.entity_id

	@staticmethod
	def write(stream, packet):
		StreamIO.write_ubyte(stream, packet.window_id)
		StreamIO.write_string(stream, packet.window_type.encode("utf8"))
		StreamIO.write_string(stream, packet.window_title.encode("utf8"))
		StreamIO.write_ubyte(stream, packet.slots_number)
		if packet.window_type == "EntityHorse":
			StreamIO.write_int(stream, packet.entity_id)

	@staticmethod
	def read(stream, packet_size):	
		window_id = StreamIO.read_ubyte(stream)
		window_type = StreamIO.read_string(stream).decode("utf8")
		window_title = StreamIO.read_string(stream).decode("utf8")
		slots_number = StreamIO.read_ubyte(stream)
		entity_id = None
		if window_type == "EntityHorse":
			entity_id = StreamIO.read_int(stream)

		return OpenWindowPacket(window_id, window_type, window_title, slots_number, entity_id)