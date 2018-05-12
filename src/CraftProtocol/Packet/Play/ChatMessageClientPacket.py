#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class ChatMessageClientPacket(BasePacket):

	PACKET_ID = 0x0F
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, chat, position):
		BasePacket.__init__(self)
		self.chat = chat
		self.position = position

	def get_chat(self):
		return self.chat

	def get_position(self):
		return self.position

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.chat.encode("utf8"))
		StreamIO.write_byte(stream, packet.position)

	@staticmethod
	def read(stream, packet_size):
		chat = StreamIO.read_string(stream).decode("utf8")
		position = StreamIO.read_byte(stream)

		return ChatMessageClientPacket(chat, position)