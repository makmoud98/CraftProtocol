#!/usr/bin/env python

from NBTBase import NBTBase
from ..StreamIO import StreamIO

class NBTTagIntArray(NBTBase):

	TYPE_ID = 0x0B

	def __init__(self, values = []):
		NBTBase.__init__(self)
		self._values = values

	def get(self):
		return self._values

	def __getitem__(self, index):
		return self._values[index]

	def __setitem__(self, index, value):
		self._values[index] = value

	def __delitem__(self, index):
		del self._values[index]

	def __iter__(self):
		return self._values.__iter__()

	def __contains__(self, item):
		return self._values.__contains__(item)

	def __len__(self):
		return len(self._values)

	def append(self, x):
		if type(x) != int:
			raise ValueError("arg must be int")

		self._values.append(x)

	def remove(self, x):
		self._values.remove(x)

	@staticmethod
	def write(stream, tag):
		StreamIO.write_int(stream, len(tag._values))
		for i in self._values:
			StreamIO.write_int(stream, i)

	@staticmethod
	def read(stream):
		values = []
		size = StreamIO.read_int(stream)

		counter = 0
		while counter < size:
			values.append(StreamIO.read_int(stream))
			counter += 1

		return NBTTagIntArray(values)