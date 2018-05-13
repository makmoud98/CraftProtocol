#!/usr/bin/env python

from ...StreamIO import StreamIO
from ...NBT import NBTSerializer
from ...ItemStack import ItemStack
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class ClickWindowPacket(BasePacket):

	PACKET_ID = 0x07
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, window_id, slot, button, action, mode, itemstack):
		BasePacket.__init__(self)
		self.window_id = window_id
		self.slot = slot
		self.button = button
		self.action = action
		self.mode = mode
		self.itemstack = itemstack

	def get_window_id(self):
		return self.window_id

	def get_slot(self):
		return self.slot

	def get_button(self):
		return self.button

	def get_action(self):
		return self.action

	def get_mode(self):
		return self.mode

	def get_itemstack(self):
		return self.itemstack

	@staticmethod
	def write(stream, packet):
		StreamIO.write_ubyte(stream, packet.window_id)
		StreamIO.write_short(stream, packet.slot)
		StreamIO.write_byte(stream, packet.button)
		StreamIO.write_short(stream, packet.action)
		StreamIO.write_varint(stream, packet.mode)
		StreamIO.write_short(stream, packet.itemstack.get_id())
		if packet.itemstack.get_id() != -1:
			StreamIO.write_byte(stream, packet.itemstack.get_count())
			StreamIO.write_short(stream, packet.itemstack.get_damage())
			NBTSerializer.write(stream, packet.itemstack.get_tag())

	@staticmethod
	def read(stream, packet_size):	
		window_id = StreamIO.read_ubyte(stream)
		slot = StreamIO.read_short(stream)
		button = StreamIO.read_byte(stream)
		action = StreamIO.read_short(stream)
		mode = StreamIO.read_varint(stream)

		id = StreamIO.read_short(stream)
		itemstack = ItemStack(id)

		if id != -1:
			itemstack.set_count(StreamIO.read_byte(stream))
			itemstack.set_damage(StreamIO.read_short(stream))
			itemstack.set_tag(NBTSerializer.read(stream))

		return ClickWindowPacket(window_id, slot, button, action, mode, itemstack)