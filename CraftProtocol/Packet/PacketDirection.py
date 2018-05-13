#!/usr/bin/env python

class PacketDirection(object):
	CLIENTBOUND = 0
	SERVERBOUND = 1

	@staticmethod
	def reverse(target):
		if target == PacketDirection.CLIENTBOUND:
			return PacketDirection.SERVERBOUND

		if target == PacketDirection.SERVERBOUND:
			return PacketDirection.CLIENTBOUND

		return None

	@staticmethod
	def to_name(target):
		if target == PacketDirection.CLIENTBOUND:
			return "Clientbound"

		if target == PacketDirection.SERVERBOUND:
			return "Serverbound"

		return None