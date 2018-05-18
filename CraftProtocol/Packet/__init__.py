#!/usr/bin/env python

import types

import Handshaking
import Login
import Play
import Status
from BasePacket import BasePacket
from PacketDirection import PacketDirection
from PacketManager import PacketManager
from PacketSerializer import PacketSerializer
from CraftProtocol.ProtocolState import ProtocolState

for name, cls in Handshaking.__dict__.items():
    if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
        PacketManager.register(ProtocolState.HANDSHAKING, cls.PACKET_DIRECTION, cls.PACKET_ID, cls)

for name, cls in Status.__dict__.items():
    if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
        PacketManager.register(ProtocolState.STATUS, cls.PACKET_DIRECTION, cls.PACKET_ID, cls)

for name, cls in Login.__dict__.items():
    if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
        PacketManager.register(ProtocolState.LOGIN, cls.PACKET_DIRECTION, cls.PACKET_ID, cls)

for name, cls in Play.__dict__.items():
    if isinstance(cls, types.TypeType) and issubclass(cls, BasePacket):
        PacketManager.register(ProtocolState.PLAY, cls.PACKET_DIRECTION, cls.PACKET_ID, cls)
