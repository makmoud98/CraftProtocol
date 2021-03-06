#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class ChatMessageServerPacket(BasePacket):
    PACKET_ID = 0x02
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, text):
        BasePacket.__init__(self)
        self._text = text

    def get_text(self):
        return self._text

    @staticmethod
    def write(stream, packet):
        StreamIO.write_string(stream, packet._text.encode("utf8"))

    @staticmethod
    def read(stream, packet_size):
        text = StreamIO.read_string(stream).decode("utf8")

        return ChatMessageServerPacket(text)
