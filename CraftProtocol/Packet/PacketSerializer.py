#!/usr/bin/env python

import types
import zlib
from cStringIO import StringIO

import Handshaking
import Login
import Play
import Status
from BasePacket import BasePacket
from PacketDirection import PacketDirection
from ..ProtocolState import ProtocolState
from ..StreamIO import StreamIO


class PacketSerializer(object):

    def __init__(self, direction):
        self._direction = direction
        self._state = ProtocolState.HANDSHAKING
        self._threshold = -1

    def set_threshold(self, value):
        self._threshold = value

    def is_compression_enabled(self):
        return self._threshold >= 0

    def get_threshold(self):
        return self._threshold

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def write(self, stream, packet):
        if packet.__class__.PACKET_DIRECTION != self._direction:
            raise ValueError(packet.__class__.__name__ + " has other direction")

        buf = StringIO()
        StreamIO.write_varint(buf, packet.__class__.PACKET_ID)
        packet.__class__.write(buf, packet)
        data = buf.getvalue()
        buf.close()

        if self.is_compression_enabled():
            buf = StringIO()

            if len(data) >= self.get_threshold():
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

        if self._state == ProtocolState.HANDSHAKING:
            for name, cls in Handshaking.__dict__.items():
                if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
                    if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self._direction:
                        packet_class = cls
                        break
        elif self._state == ProtocolState.STATUS:
            for name, cls in Status.__dict__.items():
                if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
                    if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self._direction:
                        packet_class = cls
                        break
        elif self._state == ProtocolState.LOGIN:
            for name, cls in Login.__dict__.items():
                if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
                    if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self._direction:
                        packet_class = cls
                        break
        elif self._state == ProtocolState.PLAY:
            for name, cls in Play.__dict__.items():
                if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
                    if packet_id == cls.PACKET_ID and PacketDirection.reverse(cls.PACKET_DIRECTION) == self._direction:
                        packet_class = cls
                        break

        if packet_class == None:
            buf.close()
            return BasePacket()  # Unknown packet

        packet = packet_class.read(buf, packet_size)
        buf.close()

        return packet
