#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class HandshakePacket(BasePacket):

	PACKET_ID = 0x00
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, protocol, hostname, port, next_state):
		BasePacket.__init__(self)
		self.protocol = protocol
		self.hostname = hostname
		self.port = port
		self.next_state = next_state

	def get_protocol():
		return self.protocol

	def get_hostname():
		return self.hostname

	def get_port():
		return self.port

	def get_next_state():
		return self.next_state

	@staticmethod
	def write(stream, packet):
		StreamIO.write_varint(stream, packet.protocol)
		StreamIO.write_string(stream, packet.hostname.encode("utf8"))
		StreamIO.write_ushort(stream, packet.port)
		StreamIO.write_varint(stream, packet.next_state)

	@staticmethod
	def read(stream, packet_size):
		protocol = StreamIO.read_varint(stream)
		hostname = StreamIO.read_string(stream).decode("utf8")
		port = StreamIO.read_ushort(stream)
		next_state = StreamIO.read_varint(stream)

		return HandshakePacket(protocol, hostname, port, next_state)