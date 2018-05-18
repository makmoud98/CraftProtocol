#!/usr/bin/env python

from CraftProtocol.Packet.BasePacket import BasePacket
from CraftProtocol.Packet.PacketDirection import PacketDirection
from CraftProtocol.ItemStack import ItemStack
from CraftProtocol.NBT.NBTSerializer import NBTSerializer
from CraftProtocol.StreamIO import StreamIO


class ClickWindowPacket(BasePacket):
    PACKET_ID = 0x07
    PACKET_DIRECTION = PacketDirection.SERVERBOUND

    def __init__(self, window_id, slot, button, action, mode, itemstack):
        BasePacket.__init__(self)
        self._window_id = window_id
        self._slot = slot
        self._button = button
        self._action = action
        self._mode = mode
        self._itemstack = itemstack

    def get_window_id(self):
        return self._window_id

    def get_slot(self):
        return self._slot

    def get_button(self):
        return self._button

    def get_action(self):
        return self._action

    def get_mode(self):
        return self._mode

    def get_itemstack(self):
        return self._itemstack

    @staticmethod
    def write(stream, packet):
        StreamIO.write_ubyte(stream, packet._window_id)
        StreamIO.write_short(stream, packet._slot)
        StreamIO.write_byte(stream, packet._button)
        StreamIO.write_short(stream, packet._action)
        StreamIO.write_varint(stream, packet._mode)
        StreamIO.write_short(stream, packet._itemstack.get_id())
        if packet._itemstack.get_id() != -1:
            StreamIO.write_byte(stream, packet._itemstack.get_count())
            StreamIO.write_short(stream, packet._itemstack.get_damage())
            NBTSerializer.write(stream, packet._itemstack.get_tag())

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
