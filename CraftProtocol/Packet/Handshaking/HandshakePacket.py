#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class HandshakePacket(BasePacket):

	PACKET_ID = 0x00
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, protocol, hostname, port, next_state):
		BasePacket.__init__(self)
		self._protocol = protocol
		self._hostname = hostname
		self._port = port
		self._next_state = next_state

	def get_protocol():
		return self._protocol

	def get_hostname():
		return self._hostname

	def get_port():
		return self._port

	def get_next_state():
		return self._next_state

	@staticmethod
	def write(stream, packet):
		StreamIO.write_varint(stream, packet._protocol)
		StreamIO.write_string(stream, packet._hostname.encode("utf8"))
		StreamIO.write_ushort(stream, packet._port)
		StreamIO.write_varint(stream, packet._next_state)

	@staticmethod
	def read(stream, packet_size):
		protocol = StreamIO.read_varint(stream)
		hostname = StreamIO.read_string(stream).decode("utf8")
		port = StreamIO.read_ushort(stream)
		next_state = StreamIO.read_varint(stream)

		return HandshakePacket(protocol, hostname, port, next_state)