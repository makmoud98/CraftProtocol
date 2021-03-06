#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class DisconnectPacket(BasePacket):
    PACKET_ID = 0x00
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, reason):
        BasePacket.__init__(self)
        self._reason = reason

    def get_reason(self):
        return self._reason

    @staticmethod
    def write(stream, packet):
        StreamIO.write_string(stream, packet._reason.encode("utf8"))

    @staticmethod
    def read(stream, packet_size):
        reason = StreamIO.read_string(stream).decode("utf8")

        return DisconnectPacket(reason)
