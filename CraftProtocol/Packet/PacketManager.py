#!/usr/bin/env python

from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.ProtocolState import ProtocolState


class PacketManager(object):
    _PACKETS = {
        ProtocolState.HANDSHAKING: {
            PacketDirection.SERVERBOUND: {}, PacketDirection.CLIENTBOUND: {}
        },
        ProtocolState.STATUS: {
            PacketDirection.SERVERBOUND: {}, PacketDirection.CLIENTBOUND: {}
        },
        ProtocolState.LOGIN: {
            PacketDirection.SERVERBOUND: {}, PacketDirection.CLIENTBOUND: {}
        },
        ProtocolState.PLAY: {
            PacketDirection.SERVERBOUND: {}, PacketDirection.CLIENTBOUND: {}
        }
    }

    @staticmethod
    def get(state, direction, packet_id):
        return PacketManager._PACKETS[state][direction][packet_id]

    @staticmethod
    def register(state, direction, packet_id, cls):
        if not issubclass(cls, BasePacket):
            raise ValueError("This class is not valid packet")

        if id in PacketManager._PACKETS[state][direction]:
            raise ValueError("This id is already registered")

        PacketManager._PACKETS[state][direction][packet_id] = cls
