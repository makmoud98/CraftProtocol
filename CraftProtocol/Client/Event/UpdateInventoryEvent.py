#!/usr/bin/env python

from BaseEvent import BaseEvent

class UpdateInventoryEvent(BaseEvent):

	def __init__(self, player, id, slots):
		BaseEvent.__init__(self, player)
		self._id = id
		self._slots = slots

	def get_id(self):
		return self._id

	def get_slots(self):
		return self._slots

	def set_slots(self, slots):
		self._slots = slots