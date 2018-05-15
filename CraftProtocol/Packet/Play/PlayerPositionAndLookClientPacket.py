#!/usr/bin/env python

from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection
from ...StreamIO import StreamIO


class PlayerPositionAndLookClientPacket(BasePacket):
    PACKET_ID = 0x2E
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, x, y, z, yaw, pitch, flags, teleport_id):
        BasePacket.__init__(self)
        self._x = x
        self._y = y
        self._z = z
        self._yaw = yaw
        self._pitch = pitch
        self._flags = flags
        self._teleport_id = teleport_id

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def get_yaw(self):
        return self._yaw

    def get_pitch(self):
        return self._pitch

    def get_flags(self):
        return self._flags

    def get_teleport_id(self):
        return self._teleport_id

    @staticmethod
    def write(stream, packet):
        StreamIO.write_double(stream, packet._x)
        StreamIO.write_double(stream, packet._y)
        StreamIO.write_double(stream, packet._z)
        StreamIO.write_float(stream, packet._yaw)
        StreamIO.write_float(stream, packet._pitch)
        StreamIO.write_byte(stream, packet._flags)
        StreamIO.write_varint(stream, packet._teleport_id)

    @staticmethod
    def read(stream, packet_size):
        x = StreamIO.read_double(stream)
        y = StreamIO.read_double(stream)
        z = StreamIO.read_double(stream)
        yaw = StreamIO.read_float(stream)
        pitch = StreamIO.read_float(stream)
        flags = StreamIO.read_byte(stream)
        teleport_id = StreamIO.read_varint(stream)

        return PlayerPositionAndLookClientPacket(x, y, z, yaw, pitch, flags, teleport_id)
