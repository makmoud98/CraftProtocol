#!/usr/bin/env python

import types
import sys

from NBTBase import NBTBase
from NBTSerializer import NBTSerializer
from NBTTagByte import NBTTagByte
from NBTTagByteArray import NBTTagByteArray
from NBTTagCompound import NBTTagCompound
from NBTTagDouble import NBTTagDouble
from NBTTagFloat import NBTTagFloat
from NBTTagInt import NBTTagInt
from NBTTagIntArray import NBTTagIntArray
from NBTTagList import NBTTagList
from NBTTagLong import NBTTagLong
from NBTTagLongArray import NBTTagLongArray
from NBTTagShort import NBTTagShort
from NBTTagString import NBTTagString
from NBTManager import NBTManager

for name, cls in sys.modules[__package__].__dict__.items():
    if isinstance(cls, types.TypeType) and issubclass(cls, NBTBase) and cls is not NBTBase:
       NBTManager.register(cls.TYPE_ID, cls)
