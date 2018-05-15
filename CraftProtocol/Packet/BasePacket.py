#!/usr/bin/env python


class BasePacket(object):
    PACKET_ID = None
    PACKET_DIRECTION = None

    def __init__(self):
        pass

    @staticmethod
    def write(stream, packet):
        pass

    @staticmethod
    def read(stream, packet_size):
        return BasePacket()
