#!/usr/bin/env python

class HandlerPriority(object):

	LOW = 0
	NORMAL = 1
	HIGH = 2

	@staticmethod
	def to_name(priority):
		if priority == HandlerPriority.LOW:
			return "Low"

		if priority == HandlerPriority.NORMAL:
			return "Normal"

		if priority == HandlerPriority.HIGH:
			return "High"

		if priority < HandlerPriority.LOW:
			return "Extra Low"

		if priority > HandlerPriority.HIGH:
			return "Extra High"

		return None