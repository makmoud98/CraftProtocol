#!/usr/bin/env python

from NBTBase import NBTBase
from ..StreamIO import StreamIO
import sys
import types

class NBTTagCompound(NBTBase):

	TYPE_ID = 0x0A

	def __init__(self, values = {}):
		NBTBase.__init__(self)
		self.values = values

	def get(self):
		return self.values

	def __getitem__(self, key):
		return self.values[key]

	def __setitem__(self, key, value):
		self.values[key] = value

	def __delitem__(self, key):
		del self.values[key]

	def __iter__(self):
		return self.values.__iter__()

	def __contains__(self, key):
		return self.values.__contains__(key)

	def __len__(self):
		return len(self.values)

	def keys(self):
		return self.values.keys()

	def items(self):
		return self.values.items()

	@staticmethod
	def write(stream, tag):
		for i in tag.keys():
			for name, item in sys.modules[__package__].__dict__.items():
				if isinstance(item, types.TypeType) and item != NBTBase and issubclass(item, NBTBase):
					if tag[i].__class__.TYPE_ID == item.TYPE_ID:
						StreamIO.write_ubyte(stream, tag[i].__class__.TYPE_ID)
						StreamIO.write_ushort(stream, len(i.encode("utf8")))
						StreamIO.write(stream, i.encode("utf8"))
						tag[i].__class__.write(stream, tag[i])

		StreamIO.write_ubyte(stream, 0x00)

	@staticmethod
	def read(stream):
		values = {}
		entry_type_id = StreamIO.read_ubyte(stream)

		while entry_type_id != 0x00:
			entry_name_len = StreamIO.read_ushort(stream)
			entry_name = u""
			if entry_name_len > 0:
				entry_name = StreamIO.read(stream, entry_name_len).decode("utf8")

			for name, item in sys.modules[__package__].__dict__.items():
				if isinstance(item, types.TypeType) and item != NBTBase and issubclass(item, NBTBase):
					if entry_type_id == item.TYPE_ID:
						values[entry_name] = item.read(stream)

			if not entry_name in values:
				raise IOError("Invalid NBTTagCompound entry ID = " + hex(entry_type_id))

			entry_type_id = StreamIO.read_ubyte(stream)

		return NBTTagCompound(values)