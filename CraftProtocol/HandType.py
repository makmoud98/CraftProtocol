#!/usr/bin/env python

class HandType(object):

	MAIN = 0
	OFF = 1

	@staticmethod
	def to_name(hand):
		if hand == HandType.MAIN:
			return "Main"

		if hand == HandType.OFF:
			return "Off"

		return None