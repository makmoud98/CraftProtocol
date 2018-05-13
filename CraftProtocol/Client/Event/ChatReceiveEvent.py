#!/usr/bin/env python

from BaseEvent import BaseEvent

class ChatReceiveEvent(BaseEvent):

	def __init__(self, player, text):
		BaseEvent.__init__(self, player)
		self.text = text

	def get_text(self):
		return self.text

	def set_text(self, text):
		self.text = text