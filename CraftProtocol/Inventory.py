#!/usr/bin/env python

import threading

from CraftProtocol.ItemStack import ItemStack


class Inventory(object):

    def __init__(self, inventory_id, title, inventory_type, slots_number, entity_id=None):
        self._id = inventory_id
        self._title = title
        self._type = inventory_type
        self._slots = [ItemStack.empty()] * slots_number
        self._entity_id = entity_id
        self._action_number = 1
        self._lock = threading.Lock()

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_type(self):
        return self._type

    def get_slots(self):
        return self._slots

    def get_entity_id(self):
        return self._entity_id

    def __getitem__(self, index):
        return self._slots[index]

    def __setitem__(self, index, value):
        self._slots[index] = value

    def __delitem__(self, index):
        self._slots[index] = ItemStack.empty()

    def __len__(self):
        return len(self._slots)

    def get_and_inc_action_number(self):
        with self._lock:
            action_number = self._action_number
            self._action_number += 1
            return action_number

    def get_action_number(self):
        return self._action_number

    def copy(self):
        inventory = Inventory(self._id, self._title, self._type, 0, self._entity_id)
        inventory._slots = self._slots

        return inventory
