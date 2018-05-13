#!/usr/bin/env python

from ItemStack import ItemStack
import threading

class Inventory(object):

	def __init__(self, id, title, type, slots_number, entity_id = None):
		self.id = id
		self.title = title
		self.type = type
		self.slots = [ ItemStack.empty() ] * slots_number
		self.entity_id = entity_id
		self.action_number = 1
		self.lock = threading.Lock()

	def get_id(self):
		return self.id

	def get_title(self):
		return self.title

	def get_type(self):
		return self.type

	def get_slots(self):
		return self.slots

	def get_entity_id(self):
		return self.entity_id

	def __getitem__(self, index):
		return self.slots[index]

	def __setitem__(self, index, value):
		self.slots[index] = value

	def __delitem__(self, index):
		self.slots[index] = ItemStack.empty()

	def __len__(self):
		return len(self.slots)

	def get_and_inc_action_number(self):
		with self.lock:
			action_number = self.action_number
			self.action_number += 1
			return action_number

	def get_action_number(self):
		return self.action_number

	def copy(self):
		inventory = Inventory(self.id, self.title, self.type, 0, self.entity_id)
		inventory.slots = self.slots

		return inventory