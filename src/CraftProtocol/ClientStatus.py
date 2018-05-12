#!/usr/bin/env python

class ClientStatus(object):

	RESPAWN = 0
	STATS = 1

	@staticmethod
	def to_name(status):
		if status == ClientStatus.RESPAWN:
			return "Respawn"

		if status == ClientStatus.STATS:
			return "Stats"

		return None