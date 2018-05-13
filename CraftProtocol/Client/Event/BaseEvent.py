#!/usr/bin/env python

class BaseEvent(object):

	def __init__(self, player):
		self.player = player
		self.cancelled = False

	def cancel(self):
		self.cancelled = True

	def get_player(self):
		return self.player

	def is_cancelled(self):
		return self.cancelled