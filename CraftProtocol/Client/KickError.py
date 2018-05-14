#!/usr/bin/env python

class KickError(Exception):

	def __init__(self, reason):
		self._reason = reason

	def get_reason(self):
		return self._reason

	def __str__(self):
		return self.get_reason()