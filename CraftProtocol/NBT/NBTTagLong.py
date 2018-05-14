#!/usr/bin/env python

from NBTBase import NBTBase
from ..StreamIO import StreamIO

class NBTTagLong(NBTBase):

	TYPE_ID = 0x04

	def __init__(self, value):
		NBTBase.__init__(self)
		self._value = value

	def get(self):
		return self._value

	@staticmethod
	def write(stream, tag):
		StreamIO.write_long(stream, tag._value)

	@staticmethod
	def read(stream):
		value = StreamIO.read_long(stream)

		return NBTTagLong(value)