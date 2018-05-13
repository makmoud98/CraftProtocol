#!/usr/bin/env python

from BaseEvent import BaseEvent

class UpdateInventoryEvent(BaseEvent):

	def __init__(self, id, slots):
		BaseEvent.__init__(self)
		self.id = id
		self.slots = slots

	def get_id(self):
		return self.id

	def get_slots(self):
		return self.slots

	def set_slots(self, slots):
		self.slots = slots