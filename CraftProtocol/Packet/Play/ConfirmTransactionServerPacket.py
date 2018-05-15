#!/usr/bin/env python

from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection
from ...StreamIO import StreamIO


class ConfirmTransactionServerPacket(BasePacket):
    PACKET_ID = 0x05
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, window_id, action, accepted):
        BasePacket.__init__(self)
        self._window_id = window_id
        self._action = action
        self._accepted = accepted

    def get_window_id(self):
        return self._window_id

    def get_action(self):
        return self._action

    def is_accepted(self):
        return self._accepted

    @staticmethod
    def write(stream, packet):
        StreamIO.write_byte(stream, packet._window_id)
        StreamIO.write_short(stream, packet._action)
        StreamIO.write_bool(stream, packet._accepted)

    @staticmethod
    def read(stream, packet_size):
        window_id = StreamIO.read_byte(stream)
        action = StreamIO.read_short(stream)
        accepted = StreamIO.read_bool(stream)

        return ConfirmTransactionServerPacket(window_id, action, accepted)
