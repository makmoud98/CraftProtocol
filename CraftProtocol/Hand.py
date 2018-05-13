#!/usr/bin/env python

class Hand(object):

	LEFT = 0
	RIGHT = 1

	@staticmethod
	def to_name(hand):
		if hand == Hand.LEFT:
			return "Left"

		if hand == Hand.RIGHT:
			return "Right"

		return None