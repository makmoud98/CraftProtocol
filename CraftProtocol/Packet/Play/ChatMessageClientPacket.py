#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class ChatMessageClientPacket(BasePacket):
    PACKET_ID = 0x0F
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, chat, position):
        BasePacket.__init__(self)
        self._chat = chat
        self._position = position

    def get_chat(self):
        return self._chat

    def get_position(self):
        return self._position

    @staticmethod
    def write(stream, packet):
        StreamIO.write_string(stream, packet._chat.encode("utf8"))
        StreamIO.write_byte(stream, packet._position)

    @staticmethod
    def read(stream, packet_size):
        chat = StreamIO.read_string(stream).decode("utf8")
        position = StreamIO.read_byte(stream)

        return ChatMessageClientPacket(chat, position)
