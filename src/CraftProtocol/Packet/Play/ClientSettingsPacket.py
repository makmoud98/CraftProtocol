#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class ClientSettingsPacket(BasePacket):

	PACKET_ID = 0x04
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, locale, view_distance, chat_mode, chat_colors, skin_parts, main_hand):
		BasePacket.__init__(self)
		self.locale = locale
		self.view_distance = view_distance
		self.chat_mode = chat_mode
		self.chat_colors = chat_colors
		self.skin_parts = skin_parts
		self.main_hand = main_hand

	def get_locale(self):
		return self.locale

	def get_view_distance(self):
		return self.view_distance

	def get_chat_mode(self):
		return self.chat_mode

	def is_chat_colors(self):
		return self.chat_colors

	def get_skin_parts(self):
		return self.skin_parts

	def get_main_hand(self):
		return self.main_hand

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.locale)
		StreamIO.write_byte(stream, packet.view_distance)
		StreamIO.write_varint(stream, packet.chat_mode)
		StreamIO.write_bool(stream, packet.chat_colors)
		StreamIO.write_ubyte(stream, packet.skin_parts)
		StreamIO.write_varint(stream, packet.main_hand)

	@staticmethod
	def read(stream, packet_size):	
		locale = StreamIO.read_string(stream)
		view_distance = StreamIO.read_byte(stream)
		chat_mode = StreamIO.read_varint(stream)
		chat_colors = StreamIO.read_bool(stream)
		skin_parts = StreamIO.read_ubyte(stream)
		main_hand = StreamIO.read_varint(stream)

		return ClientSettingsPacket(locale, view_distance, chat_mode, chat_colors, skin_parts, main_hand)