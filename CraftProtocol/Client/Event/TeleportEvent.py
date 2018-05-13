#!/usr/bin/env python

from BaseEvent import BaseEvent

class TeleportEvent(BaseEvent):

	def __init__(self, x, y, z, teleport_id):
		BaseEvent.__init__(self)
		self.x = x
		self.y = y
		self.z = z
		self.teleport_id = teleport_id

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_z(self):
		return self.z

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def set_z(self, z):
		self.z = z

	def get_teleport_id(self):
		return self.teleport_id