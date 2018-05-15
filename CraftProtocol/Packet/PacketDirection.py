#!/usr/bin/env python


class PacketDirection(object):
    CLIENTBOUND = 0
    SERVERBOUND = 1

    @staticmethod
    def reverse(target):
        if target == PacketDirection.CLIENTBOUND:
            return PacketDirection.SERVERBOUND
        elif target == PacketDirection.SERVERBOUND:
            return PacketDirection.CLIENTBOUND

        return None
