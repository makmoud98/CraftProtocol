#!/usr/bin/env python

from BaseEvent import BaseEvent


class TeleportEvent(BaseEvent):

    def __init__(self, player, x, y, z, teleport_id):
        BaseEvent.__init__(self, player)
        self._x = x
        self._y = y
        self._z = z
        self._teleport_id = teleport_id

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_z(self, z):
        self._z = z

    def get_teleport_id(self):
        return self._teleport_id
