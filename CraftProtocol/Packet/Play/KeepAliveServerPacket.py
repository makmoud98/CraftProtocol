#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class KeepAliveServerPacket(BasePacket):
    PACKET_ID = 0x0B
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, id):
        BasePacket.__init__(self)
        self._id = id

    def get_id(self):
        return self._id

    @staticmethod
    def write(stream, packet):
        StreamIO.write_varint(stream, packet._id)

    @staticmethod
    def read(stream, packet_size):
        id = StreamIO.read_varint(stream)

        return KeepAliveServerPacket(id)
