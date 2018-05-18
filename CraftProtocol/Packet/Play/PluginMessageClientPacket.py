#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class PluginMessageClientPacket(BasePacket):
    PACKET_ID = 0x18
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, channel, bytes):
        BasePacket.__init__(self)
        self._channel = channel
        self._bytes = bytes

    def get_channel(self):
        return self._channel

    def get_bytes(self):
        return self._bytes

    @staticmethod
    def write(stream, packet):
        StreamIO.write_string(stream, packet._channel.encode("utf8"))
        StreamIO.write(stream, packet._bytes)

    @staticmethod
    def read(stream, packet_size):
        channel_len = StreamIO.read_varint(stream)
        channel = StreamIO.read(stream, channel_len).decode("utf8")
        bytes = StreamIO.read(stream, packet_size - StreamIO.size_varint(channel_len) - channel_len)

        return PluginMessageClientPacket(channel, bytes)
