#!/usr/bin/env python

from BaseEvent import BaseEvent


class LoginEvent(BaseEvent):

    def __init__(self, player, entity_id, gamemode, dimension, difficulty, max_players, level_type, debug_info):
        BaseEvent.__init__(self, player)
        self._entity_id = entity_id
        self._gamemode = gamemode
        self._dimension = dimension
        self._difficulty = difficulty
        self._max_players = max_players
        self._level_type = level_type
        self._debug_info = debug_info

    def get_entity_id(self):
        return self._entity_id

    def get_gamemode(self):
        return self._gamemode

    def get_dimension(self):
        return self._dimension

    def get_difficulty(self):
        return self._difficulty

    def get_max_players(self):
        return self._max_players

    def get_level_type(self):
        return self._level_type

    def get_debug_info(self):
        return self._debug_info
