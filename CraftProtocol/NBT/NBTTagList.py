#!/usr/bin/env python

from NBTBase import NBTBase
from NBTTagCompound import NBTTagCompound
from ..StreamIO import StreamIO
import sys
import types

class NBTTagList(NBTBase):

	TYPE_ID = 0x09

	def __init__(self, type, values = []):
		NBTBase.__init__(self)
		self.type = type
		self.values = values

	def get(self):
		return self.values

	def get_type(self):
		return self.type

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
		if x.__class__ != self.tag.type:
			raise ValueError("arg must be " + self.tag.type.__name__)
			
		self.values.append(x)

	def remove(self, x):
		self.values.remove(x)

	@staticmethod
	def write(stream, tag):
		StreamIO.write_ubyte(stream, tag.type.TYPE_ID)
		StreamIO.write_int(stream, len(tag.values))

		for i in tag.values:
			tag.type.write(stream, i)

	@staticmethod
	def read(stream):
		type_id = StreamIO.read_ubyte(stream)
		type = None
		values = []

		for name, item in sys.modules[__package__].__dict__.items():
			if isinstance(item, types.TypeType) and item != NBTBase and issubclass(item, NBTBase):
				if type_id == item.TYPE_ID:
					type = item
					break

		if type == None:
			raise IOError("Invalid NBTTagList type ID = " + hex(type_id))

		values_len = StreamIO.read_int(stream)
		for i in range(values_len):
			values.append(type.read(stream))

		return NBTTagList(type, values)