#!/usr/bin/env python

from BaseEvent import BaseEvent

class LoginEvent(BaseEvent):

	def __init__(self, player, entity_id, gamemode, dimension, difficulty, max_players, level_type, debug_info):
		BaseEvent.__init__(self, player)
		self.entity_id = entity_id
		self.gamemode = gamemode
		self.dimension = dimension
		self.difficulty = difficulty
		self.max_players = max_players
		self.level_type = level_type
		self.debug_info = debug_info

	def get_entity_id(self):
		return self.entity_id

	def get_gamemode(self):
		return self.gamemode

	def get_dimension(self):
		return self.dimension

	def get_difficulty(self):
		return self.difficulty

	def get_max_players(self):
		return self.max_players

	def get_level_type(self):
		return self.level_type

	def get_debug_info(self):
		return self.debug_info