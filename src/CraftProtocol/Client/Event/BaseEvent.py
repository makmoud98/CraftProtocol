#!/usr/bin/env python

class BaseEvent(object):

	def __init__(self):
		self.cancelled = False

	def cancel(self):
		self.cancelled = True

	def is_cancelled(self):
		return self.cancelled