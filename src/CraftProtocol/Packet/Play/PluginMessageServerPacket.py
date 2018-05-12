#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class PluginMessageServerPacket(BasePacket):

	PACKET_ID = 0x09
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, channel, bytes):
		BasePacket.__init__(self)
		self.channel = channel
		self.bytes = bytes

	def get_channel(self):
		return self.channel

	def get_bytes(self):
		return self.bytes

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.channel.encode("utf8"))
		StreamIO.write(stream, packet.bytes)

	@staticmethod
	def read(stream, packet_size):
		channel_len = StreamIO.read_varint(stream)
		channel = StreamIO.read(stream, channel_len).decode("utf8")
		bytes = StreamIO.read(stream, packet_size - StreamIO.size_varint(channel_len) - channel_len)

		return PluginMessageServerPacket(channel, bytes)