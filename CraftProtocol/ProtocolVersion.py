#!/usr/bin/env python

class ProtocolVersion(object):

	MC_1_10 = 210

	@staticmethod
	def to_name(protocol):
		if protocol == ProtocolVersion.MC_1_10:
			return "1.10.x"

		return None