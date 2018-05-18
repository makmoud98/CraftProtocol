#!/usr/bin/env python

from CraftProtocol.Client.Event import BaseEvent


class ChatSendEvent(BaseEvent):

    def __init__(self, player, text):
        BaseEvent.__init__(self, player)
        self._text = text

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
