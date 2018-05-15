#!/usr/bin/env python

import CraftProtocol


class ChatBot(object):

    def __init__(self, player):
        self._player = player
        self._player.register_listener(CraftProtocol.Client.Event.DisconnectEvent, self.on_disconnect)
        self._player.register_listener(CraftProtocol.Client.Event.ChatReceiveEvent, self.on_chat)

    def get_player(self):
        return self._player

    @CraftProtocol.Client.Event.Handler
    def on_chat(self, event):
        print CraftProtocol.ChatSerializer.strip_colors(event.get_text())

    @CraftProtocol.Client.Event.Handler
    def on_disconnect(self, event):
        print "Disconnected: " + event.get_reason()


def main():
    server = CraftProtocol.Client.CraftServer("localhost", 25565, CraftProtocol.ProtocolVersion.MC_1_10)
    server.ping()
    player = None
    try:
        player = server.login("ChatBot")
    except CraftProtocol.Client.KickError as ex:
        print "Kicked: " + ex.get_reason()
        return

    bot = ChatBot(player)
    try:
        bot.get_player().loop()
    except KeyboardInterrupt:
        bot.get_player().disconnect("Bye")


if __name__ == "__main__": main()
