#!/usr/bin/env python

from BaseEvent import BaseEvent

class OpenInventoryEvent(BaseEvent):

	def __init__(self, inventory):
		BaseEvent.__init__(self)
		self.inventory = inventory

	def get_inventory(self):
		return self.inventory