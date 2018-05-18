#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class ResponsePacket(BasePacket):
    PACKET_ID = 0x00
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, json):
        BasePacket.__init__(self)
        self._json = json

    def get_json(self):
        return self._json

    @staticmethod
    def write(stream, packet):
        StreamIO.write_string(stream, packet._json.encode("utf8"))

    @staticmethod
    def read(stream, packet_size):
        json = StreamIO.read_string(stream).decode("utf8")

        return ResponsePacket(json)
