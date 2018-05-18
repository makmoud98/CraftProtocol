#!/usr/bin/env python

from CraftProtocol.Client.Event import BaseEvent


class UpdateInventoryEvent(BaseEvent):

    def __init__(self, player, inventory, slots):
        BaseEvent.__init__(self, player)
        self._inventory = inventory
        self._slots = slots

    def get_inventory(self):
        return self._inventory

    def get_slots(self):
        return self._slots

    def set_slots(self, slots):
        self._slots = slots
