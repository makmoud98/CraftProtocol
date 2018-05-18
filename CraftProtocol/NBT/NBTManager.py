#!/usr/bin/env python

from CraftProtocol.NBT.NBTBase import NBTBase


class NBTManager(object):
    _TAGS = {}

    @staticmethod
    def get(type_id):
        return NBTManager._TAGS[type_id]

    @staticmethod
    def register(type_id, cls):
        if not issubclass(cls, NBTBase):
            raise ValueError("This class is not valid NBT tag")

        if id in NBTManager._TAGS:
            raise ValueError("This id is already registered")

        NBTManager._TAGS[type_id] = cls