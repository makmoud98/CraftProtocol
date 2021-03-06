#!/usr/bin/env python

from CraftProtocol.StreamIO import StreamIO
from CraftProtocol.NBT.NBTBase import NBTBase
from CraftProtocol.NBT.NBTManager import NBTManager


class NBTTagCompound(NBTBase):
    TYPE_ID = 0x0A

    def __init__(self, values={}):
        NBTBase.__init__(self)
        self._values = values

    def get(self):
        return self._values

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __delitem__(self, key):
        del self._values[key]

    def __iter__(self):
        return self._values.__iter__()

    def __contains__(self, key):
        return self._values.__contains__(key)

    def __len__(self):
        return len(self._values)

    def keys(self):
        return self._values.keys()

    def items(self):
        return self._values.items()

    @staticmethod
    def write(stream, tag):
        for i in tag.keys():
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

            entry_type = NBTManager.get(entry_type_id)

            values[entry_name] = entry_type.read(stream)
            entry_type_id = StreamIO.read_ubyte(stream)

        return NBTTagCompound(values)
