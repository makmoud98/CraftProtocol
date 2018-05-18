#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class PlayerPositionServerPacket(BasePacket):
    PACKET_ID = 0x0C
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, x, y, z, on_ground):
        BasePacket.__init__(self)
        self._x = x
        self._y = y
        self._z = z
        self._on_ground = on_ground

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def is_on_ground(self):
        return self._on_ground

    @staticmethod
    def write(stream, packet):
        StreamIO.write_double(stream, packet._x)
        StreamIO.write_double(stream, packet._y)
        StreamIO.write_double(stream, packet._z)
        StreamIO.write_bool(stream, packet._on_ground)

    @staticmethod
    def read(stream, packet_size):
        x = StreamIO.read_double(stream)
        y = StreamIO.read_double(stream)
        z = StreamIO.read_double(stream)
        on_ground = StreamIO.read_bool(stream)

        return PlayerPositionServerPacket(x, y, z, on_ground)
