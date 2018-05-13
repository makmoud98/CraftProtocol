#!/usr/bin/env python

import CraftProtocol

class ChatBot(object):

	def __init__(self, player):
		self.player = player
		self.player.register_listener(CraftProtocol.Client.Event.DisconnectEvent, self.on_disconnect)
		self.player.register_listener(CraftProtocol.Client.Event.ChatReceiveEvent, self.on_chat)

	def get_player(self):
		return self.player

	def loop(self):
		self.player.loop()

	@CraftProtocol.Client.Event.Handler
	def on_chat(self, event):
		print CraftProtocol.ChatSerializer.strip_colors(event.get_text())

	@CraftProtocol.Client.Event.Handler
	def on_disconnect(self, event):
		print "Disconnected: " + event.get_reason()

def main():
	server = CraftProtocol.Client.CraftServer("localhost", 25565)
	server.ping()
	player = None
	try:
		player = server.login("ChatBot")
	except CraftProtocol.Client.KickError as ex:
		print "Kicked: " + ex.get_reason()
		return

	bot = ChatBot(player)
	try:
		bot.loop()
	except KeyboardInterrupt:
		bot.get_player().disconnect("Bye")

if __name__ == "__main__": main()