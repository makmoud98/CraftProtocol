#!/usr/bin/env python

from BaseEvent import BaseEvent


class DisconnectEvent(BaseEvent):

    def __init__(self, player, reason):
        BaseEvent.__init__(self, player)
        self._reason = reason

    def get_reason(self):
        return self._reason

    def cancel(self):
        raise ValueError("DisconnectEvent cannot be cancelled")
