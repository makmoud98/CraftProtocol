#!/usr/bin/env python

class ItemStack(object):

	def __init__(self, id, count = 0, damage = 0, tag = None):
		self._id = id
		self._count = count
		self._damage = damage
		self._tag = tag

	@staticmethod
	def empty():
		return ItemStack(-1)

	def get_id(self):
		return self._id

	def get_count(self):
		return self._count

	def set_count(self, count):
		self._count = count

	def get_damage(self):
		return self._damage

	def set_damage(self, damage):
		self._damage = damage

	def get_tag(self):
		return self._tag

	def set_tag(self, tag):
		self._tag = tag

	def has_tag(self):
		return self._tag != None