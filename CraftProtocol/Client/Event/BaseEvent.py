#!/usr/bin/env python

class BaseEvent(object):

	def __init__(self, player):
		self._player = player
		self._cancelled = False

	def cancel(self):
		self._cancelled = True

	def get_player(self):
		return self._player

	def is_cancelled(self):
		return self._cancelled