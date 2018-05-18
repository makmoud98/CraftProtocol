#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class ClientStatusPacket(BasePacket):
    PACKET_ID = 0x03
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, action):
        BasePacket.__init__(self)
        self.action = action

    def get_action(self):
        return self.action

    @staticmethod
    def write(stream, packet):
        StreamIO.write_varint(stream, packet.action)

    @staticmethod
    def read(stream, packet_size):
        action = StreamIO.read_varint(stream)

        return ClientStatusPacket(action)
