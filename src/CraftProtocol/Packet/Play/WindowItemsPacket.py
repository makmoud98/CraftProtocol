#!/usr/bin/env python

from ...StreamIO import StreamIO
from ...NBT import NBTSerializer
from ...ItemStack import ItemStack
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class WindowItemsPacket(BasePacket):

	PACKET_ID = 0x14
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, window_id, slots):
		BasePacket.__init__(self)
		self.window_id = window_id
		self.slots = slots

	def get_window_id(self):
		return self.window_id

	def get_slots(self):
		return self.slots

	@staticmethod
	def write(stream, packet):
		StreamIO.write_ubyte(stream, packet.window_id)
		StreamIO.write_short(stream, len(packet.slots))
		for i in packet.slots:
			StreamIO.write_short(stream, i.get_id())
			if i.get_id() != -1:
				StreamIO.write_byte(stream, i.get_count())
				StreamIO.write_short(stream, i.get_damage())
				NBTSerializer.write(stream, i.get_tag())

	@staticmethod
	def read(stream, packet_size):
		window_id = StreamIO.read_ubyte(stream)
		slots_size = StreamIO.read_short(stream)
		slots = []

		while len(slots) < slots_size:
			id = StreamIO.read_short(stream)
			if id == -1:
				slots.append(ItemStack.empty())
				continue

			count = StreamIO.read_byte(stream)
			damage = StreamIO.read_short(stream)
			tag = NBTSerializer.read(stream)

			slots.append(ItemStack(id, count, damage, tag))

		return WindowItemsPacket(window_id, slots)