#!/usr/bin/env python

from NBTBase import NBTBase
from ..StreamIO import StreamIO

class NBTTagByte(NBTBase):

	TYPE_ID = 0x01

	def __init__(self, value):
		NBTBase.__init__(self)
		self.value = value

	def get(self):
		return self.value

	@staticmethod
	def write(stream, tag):
		StreamIO.write_byte(tag.value)

	@staticmethod
	def read(stream):
		value = StreamIO.read_byte(stream)

		return NBTTagByte(value)