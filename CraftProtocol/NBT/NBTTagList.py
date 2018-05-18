#!/usr/bin/env python

from CraftProtocol.NBT.NBTBase import NBTBase
from CraftProtocol.NBT.NBTManager import NBTManager
from CraftProtocol.StreamIO import StreamIO


class NBTTagList(NBTBase):
    TYPE_ID = 0x09

    def __init__(self, type_tag, values=[]):
        NBTBase.__init__(self)
        self._type_tag = type_tag
        self._values = values

    def get(self):
        return self._values

    def get_type_tag(self):
        return self._type_tag

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
        if x.__class__ != self._type_tag:
            raise ValueError("arg must be " + self._type_tag.__name__)

        self._values.append(x)

    def remove(self, x):
        self._values.remove(x)

    @staticmethod
    def write(stream, tag):
        StreamIO.write_ubyte(stream, tag._type_tag.TYPE_ID)
        StreamIO.write_int(stream, len(tag._values))

        for i in tag._values:
            tag._type_tag.write(stream, i)

    @staticmethod
    def read(stream):
        type_id = StreamIO.read_ubyte(stream)
        values = []

        tag_type = NBTManager.get(type_id)

        values_len = StreamIO.read_int(stream)
        for i in range(values_len):
            values.append(tag_type.read(stream))

        return NBTTagList(tag_type, values)
