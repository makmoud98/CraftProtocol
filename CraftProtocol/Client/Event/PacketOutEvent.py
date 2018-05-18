#!/usr/bin/env python

from CraftProtocol.Client.Event import BaseEvent


class PacketOutEvent(BaseEvent):

    def __init__(self, player, packet):
        BaseEvent.__init__(self, player)
        self._packet = packet

    def get_packet(self):
        return self._packet

    def set_packet(self, packet):
        self._packet = packet
