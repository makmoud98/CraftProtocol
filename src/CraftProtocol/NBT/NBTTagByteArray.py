#!/usr/bin/env python

from NBTBase import NBTBase
from ..StreamIO import StreamIO

class NBTTagByteArray(NBTBase):

	TYPE_ID = 0x07

	def __init__(self, values = []):
		NBTBase.__init__(self)
		self.values = values

	def get(self):
		return self.values

	def __getitem__(self, index):
		return self.values[index]

	def __setitem__(self, index, value):
		self.values[index] = value

	def __delitem__(self, index):
		del self.values[index]

	def __iter__(self):
		return self.values.__iter__()

	def __contains__(self, item):
		return self.values.__contains__(item)

	def __len__(self):
		return len(self.values)

	def append(self, x):
		if type(x) != int:
			raise ValueError("arg must be int")

		self.values.append(x)

	def remove(self, x):
		self.values.remove(x)

	@staticmethod
	def write(stream, tag):
		StreamIO.write_int(stream, len(tag.values))
		for i in self.values:
			StreamIO.write_byte(stream, i)

	@staticmethod
	def read(stream):
		values = []
		size = StreamIO.read_int(stream)

		counter = 0
		while counter < size:
			values.append(StreamIO.read_byte(stream))
			counter += 1

		return NBTTagByteArray(values)