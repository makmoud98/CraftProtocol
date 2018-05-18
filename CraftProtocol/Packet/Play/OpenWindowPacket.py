#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class OpenWindowPacket(BasePacket):
    PACKET_ID = 0x13
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, window_id, window_type, window_title, slots_number, entity_id):
        BasePacket.__init__(self)
        self._window_id = window_id
        self._window_type = window_type
        self._window_title = window_title
        self._slots_number = slots_number
        self._entity_id = entity_id

    def get_window_id(self):
        return self._window_id

    def get_window_type(self):
        return self._window_type

    def get_window_title(self):
        return self._window_title

    def get_slots_number(self):
        return self._slots_number

    def get_entity_id(self):
        return self._entity_id

    @staticmethod
    def write(stream, packet):
        StreamIO.write_ubyte(stream, packet._window_id)
        StreamIO.write_string(stream, packet._window_type.encode("utf8"))
        StreamIO.write_string(stream, packet._window_title.encode("utf8"))
        StreamIO.write_ubyte(stream, packet._slots_number)
        if packet.window_type == "EntityHorse":
            StreamIO.write_int(stream, packet._entity_id)

    @staticmethod
    def read(stream, packet_size):
        window_id = StreamIO.read_ubyte(stream)
        window_type = StreamIO.read_string(stream).decode("utf8")
        window_title = StreamIO.read_string(stream).decode("utf8")
        slots_number = StreamIO.read_ubyte(stream)
        entity_id = None
        if window_type == "EntityHorse":
            entity_id = StreamIO.read_int(stream)

        return OpenWindowPacket(window_id, window_type, window_title, slots_number, entity_id)
