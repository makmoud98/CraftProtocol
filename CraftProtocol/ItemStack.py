#!/usr/bin/env python

class ItemStack(object):

	def __init__(self, id, count = 0, damage = 0, tag = None):
		self.id = id
		self.count = count
		self.damage = damage
		self.tag = tag

	@staticmethod
	def empty():
		return ItemStack(-1)

	def get_id(self):
		return self.id

	def get_count(self):
		return self.count

	def set_count(self, count):
		self.count = count

	def get_damage(self):
		return self.damage

	def set_damage(self, damage):
		self.damage = damage

	def get_tag(self):
		return self.tag

	def set_tag(self, tag):
		self.tag = tag

	def has_tag(self):
		return self.tag != None