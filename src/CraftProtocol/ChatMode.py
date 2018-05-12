#!/usr/bin/env python

class ChatMode(object):

	ENABLED = 0
	COMMANDS = 1
	HIDDEN = 2

	@staticmethod
	def to_name(chat_mode):
		if chat_mode == ChatMode.ENABLED:
			return "Enabled"

		if chat_mode == ChatMode.COMMANDS:
			return "Commands"

		if chat_mode == ChatMode.HIDDEN:
			return "Hidden"

		return None