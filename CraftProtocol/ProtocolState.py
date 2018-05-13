#!/usr/bin/env python

class ProtocolState(object):
	HANDSHAKING = 0
	STATUS = 1
	LOGIN = 2
	PLAY = 3

	@staticmethod
	def to_name(state):
		if state == ProtocolState.HANDSHAKING:
			return "Handshaking"

		if state == ProtocolState.STATUS:
			return "Status"

		if state == ProtocolState.LOGIN:
			return "Login"

		if state == ProtocolState.PLAY:
			return "Play"

		return None