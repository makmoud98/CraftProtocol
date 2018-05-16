#!/usr/bin/env python

class NBTManager(object):
    _TAGS = {}

    @staticmethod
    def get(type_id):
        return NBTManager._TAGS[type_id]

    @staticmethod
    def register(type_id, cls):
        if id in NBTManager._TAGS:
            raise ValueError("This id is already registered")

        NBTManager._TAGS[type_id] = cls