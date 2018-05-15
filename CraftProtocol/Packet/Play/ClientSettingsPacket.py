#!/usr/bin/env python

from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection
from ...StreamIO import StreamIO


class ClientSettingsPacket(BasePacket):
    PACKET_ID = 0x04
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, locale, view_distance, chat_mode, chat_colors, skin_parts, main_hand):
        BasePacket.__init__(self)
        self._locale = locale
        self._view_distance = view_distance
        self._chat_mode = chat_mode
        self._chat_colors = chat_colors
        self._skin_parts = skin_parts
        self._main_hand = main_hand

    def get_locale(self):
        return self._locale

    def get_view_distance(self):
        return self._view_distance

    def get_chat_mode(self):
        return self._chat_mode

    def is_chat_colors(self):
        return self._chat_colors

    def get_skin_parts(self):
        return self._skin_parts

    def get_main_hand(self):
        return self._main_hand

    @staticmethod
    def write(stream, packet):
        StreamIO.write_string(stream, packet._locale)
        StreamIO.write_byte(stream, packet._view_distance)
        StreamIO.write_varint(stream, packet._chat_mode)
        StreamIO.write_bool(stream, packet._chat_colors)
        StreamIO.write_ubyte(stream, packet._skin_parts)
        StreamIO.write_varint(stream, packet._main_hand)

    @staticmethod
    def read(stream, packet_size):
        locale = StreamIO.read_string(stream)
        view_distance = StreamIO.read_byte(stream)
        chat_mode = StreamIO.read_varint(stream)
        chat_colors = StreamIO.read_bool(stream)
        skin_parts = StreamIO.read_ubyte(stream)
        main_hand = StreamIO.read_varint(stream)

        return ClientSettingsPacket(locale, view_distance, chat_mode, chat_colors, skin_parts, main_hand)
