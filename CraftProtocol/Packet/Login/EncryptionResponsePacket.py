#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.StreamIO import StreamIO


class EncryptionResponsePacket(BasePacket):
    PACKET_ID = 0x01
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, shared_secret, verify_token):
        BasePacket.__init__(self)
        self._shared_secret = shared_secret
        self._verify_token = verify_token

    def get_shared_secret(self):
        return self._shared_secret

    def get_verify_token(self):
        return self._verify_token

    @staticmethod
    def write(stream, packet):
        StreamIO.write_string(stream, packet._shared_secret)
        StreamIO.write_string(stream, packet._verify_token)

    @staticmethod
    def read(stream, packet_size):
        shared_secret = StreamIO.read_string(stream)
        verify_token = StreamIO.read_string(stream)

        return EncryptionResponsePacket(shared_secret, verify_token)
