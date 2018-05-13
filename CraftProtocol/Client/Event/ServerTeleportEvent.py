#!/usr/bin/env python

from BaseEvent import BaseEvent

class ServerTeleportEvent(BaseEvent):

	def __init__(self):
		BaseEvent.__init__(self)