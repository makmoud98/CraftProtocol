#!/usr/bin/env python

from ..StreamIO import StreamIO
from cStringIO import StringIO
from ..ProtocolState import ProtocolState
from PacketDirection import PacketDirection
from BasePacket import BasePacket
import Handshaking
import Status
import Login
import Play
import zlib
import time
import types

class PacketSerializer(object):

	def __init__(self, direction):
		self.direction = direction
		self.state = ProtocolState.HANDSHAKING
		self.threshold = -1

	def set_threshold(self, value):
		self.threshold = value

	def is_compression_enabled(self):
		return self.threshold >= 0

	def get_threshold(self):
		return self.threshold

	def set_state(self, state):
		self.state = state

	def get_state(self):
		return self.state

	def write(self, stream, packet):
		if packet.__class__.PACKET_DIRECTION != self.direction:
			raise ValueError(packet_class.__name__ + " has other direction")

		buf = StringIO()
		StreamIO.write_varint(buf, packet.__class__.PACKET_ID)
		packet.__class__.write(buf, packet)
		data = buf.getvalue()
		buf.close()

		if self.is_compression_enabled():
			buf = StringIO()

			if len(data) >= self.threshold:
				StreamIO.write_varint(buf, len(data))
				data = zlib.compress(data)
			else:
				StreamIO.write_varint(buf, 0)

			StreamIO.write(buf, data)
			data = buf.getvalue()
			buf.close()

		buf = StringIO()
		StreamIO.write_string(buf, data)
		data = buf.getvalue()
		buf.close()

		StreamIO.write(stream, data)

	def read(self, stream):
		packet_size = StreamIO.read_varint(stream)
		if self.is_compression_enabled():
			data_size = StreamIO.read_varint(stream)

			if data_size == 0:
				packet_size -= StreamIO.size_varint(0)
				data = StreamIO.read(stream, packet_size)
			else:
				data = StreamIO.read(stream, packet_size - StreamIO.size_varint(data_size))
				data = zlib.decompress(data)
				packet_size = data_size
		else:
			data = StreamIO.read(stream, packet_size)

		buf = StringIO(data)
		packet_id = StreamIO.read_varint(buf)
		packet_size -= StreamIO.size_varint(packet_id)
		packet_class = None

		if self.state == ProtocolState.HANDSHAKING:
			for name, cls in Handshaking.__dict__.items():
				if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
					if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self.direction:
						packet_class = cls
						break
		elif self.state == ProtocolState.STATUS:
			for name, cls in Status.__dict__.items():
				if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
					if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self.direction:
						packet_class = cls
						break
		elif self.state == ProtocolState.LOGIN:
			for name, cls in Login.__dict__.items():
				if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
					if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self.direction:
						packet_class = cls
						break
		elif self.state == ProtocolState.PLAY:
			for name, cls in Play.__dict__.items():
				if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
					if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self.direction:
						packet_class = cls
						break

		if packet_class == None:
			buf.close()
			return BasePacket() # Unknown packet

		packet = packet_class.read(buf, packet_size)
		buf.close()

		return packet