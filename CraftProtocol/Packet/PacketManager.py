#!/usr/bin/env python

from PacketDirection import PacketDirection
from ..ProtocolState import ProtocolState


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
    def get(state, direction, id):
        return PacketManager._PACKETS[state][direction][id]

    @staticmethod
    def register(state, direction, id, cls):
        if id in PacketManager._PACKETS[state][direction]:
            raise ValueError("This id is already registered")

        PacketManager._PACKETS[state][direction][id] = cls
