#!/usr/bin/env python

from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection
from ...StreamIO import StreamIO


class UseItemPacket(BasePacket):
    PACKET_ID = 0x1D
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, hand_type):
        BasePacket.__init__(self)
        self._hand_type = hand_type

    def get_hand(self):
        return self._hand_type

    @staticmethod
    def write(stream, packet):
        StreamIO.write_varint(stream, packet._hand_type)

    @staticmethod
    def read(stream, packet_size):
        hand_type = StreamIO.read_varint(stream)

        return UseItemPacket(hand_type)
