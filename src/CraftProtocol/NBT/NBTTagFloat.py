#!/usr/bin/env python

from NBTBase import NBTBase
from ..StreamIO import StreamIO

class NBTTagFloat(NBTBase):

	TYPE_ID = 0x05

	def __init__(self, value):
		NBTBase.__init__(self)
		self.value = value

	def get(self):
		return self.value

	@staticmethod
	def write(stream, tag):
		StreamIO.write_float(stream, tag.value)

	@staticmethod
	def read(stream):
		value = StreamIO.read_float(stream)

		return NBTTagFloat(value)