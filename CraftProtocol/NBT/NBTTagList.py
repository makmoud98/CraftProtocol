#!/usr/bin/env python

import sys
import types

from NBTBase import NBTBase
from ..StreamIO import StreamIO


class NBTTagList(NBTBase):
    TYPE_ID = 0x09

    def __init__(self, type, values=[]):
        NBTBase.__init__(self)
        self._type = type
        self._values = values

    def get(self):
        return self._values

    def get_type(self):
        return self._type

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
        if x.__class__ != self._type:
            raise ValueError("arg must be " + self._type.__name__)

        self._values.append(x)

    def remove(self, x):
        self._values.remove(x)

    @staticmethod
    def write(stream, tag):
        StreamIO.write_ubyte(stream, tag._type.TYPE_ID)
        StreamIO.write_int(stream, len(tag._values))

        for i in tag._values:
            tag._type.write(stream, i)

    @staticmethod
    def read(stream):
        type_id = StreamIO.read_ubyte(stream)
        type = None
        values = []

        for name, cls in sys.modules[__package__].__dict__.items():
            if isinstance(cls, types.TypeType) and issubclass(cls, NBTBase):
                if type_id == cls.TYPE_ID:
                    type = cls
                    break

        if type == None:
            raise IOError("Invalid NBTTagList type ID = " + hex(type_id))

        values_len = StreamIO.read_int(stream)
        for i in range(values_len):
            values.append(type.read(stream))

        return NBTTagList(type, values)
