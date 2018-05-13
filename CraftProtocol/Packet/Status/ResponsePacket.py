#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class ResponsePacket(BasePacket):

	PACKET_ID = 0x00
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, json):
		BasePacket.__init__(self)
		self.json = json

	def get_json(self):
		return self.json

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.json.encode("utf8"))

	@staticmethod
	def read(stream, packet_size):
		json = StreamIO.read_string(stream).decode("utf8")

		return ResponsePacket(json)