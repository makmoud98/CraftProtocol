#!/usr/bin/env python

from NBTBase import NBTBase
from ..StreamIO import StreamIO

class NBTTagString(NBTBase):

	TYPE_ID = 0x08

	def __init__(self, value):
		NBTBase.__init__(self)
		self.value = value

	def get(self):
		return self.value

	@staticmethod
	def write(stream, tag):
		StreamIO.write_ushort(stream, len(tag.value.encode("utf8")))
		StreamIO.write(stream, tag.value.encode("utf8"))

	@staticmethod
	def read(stream):
		size = StreamIO.read_ushort(stream)
		value = StreamIO.read(stream, size).decode("utf8")

		return NBTTagString(value)