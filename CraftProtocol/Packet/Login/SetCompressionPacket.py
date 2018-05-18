#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class SetCompressionPacket(BasePacket):
    PACKET_ID = 0x03
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, threshold):
        BasePacket.__init__(self)
        self._threshold = threshold

    def get_threshold(self):
        return self._threshold

    @staticmethod
    def write(stream, packet):
        StreamIO.write_varint(stream, packet._threshold)

    @staticmethod
    def read(stream, packet_size):
        threshold = StreamIO.read_varint(stream)

        return SetCompressionPacket(threshold)
