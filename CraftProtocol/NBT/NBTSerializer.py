#!/usr/bin/env python

import sys
import types

from NBTTagCompound import NBTTagCompound
from ..StreamIO import StreamIO


class NBTSerializer(object):

    @staticmethod
    def read(stream):
        compound_id = StreamIO.read_ubyte(stream)
        if compound_id == 0x00:
            return None

        if compound_id != NBTTagCompound.TYPE_ID:
            raise IOError("Invalid NBTTagCompound type ID = " + hex(compound_id))

        name_len = StreamIO.read_ushort(stream)

        name = u""
        if name_len > 0:
            name = StreamIO.read(stream, name_len)

        return NBTTagCompound.read(stream)

    @staticmethod
    def write(stream, tag):
        if tag == None:
            StreamIO.write_ubyte(0x00)
            return

        StreamIO.write_ubyte(stream, NBTTagCompound.TYPE_ID)
        StreamIO.write_ushort(stream, 0)  # Empty name

        NBTTagCompound.write(stream, tag)
