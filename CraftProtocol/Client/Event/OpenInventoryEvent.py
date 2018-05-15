#!/usr/bin/env python

from BaseEvent import BaseEvent


class OpenInventoryEvent(BaseEvent):

    def __init__(self, player, inventory):
        BaseEvent.__init__(self, player)
        self._inventory = inventory

    def get_inventory(self):
        return self._inventory
