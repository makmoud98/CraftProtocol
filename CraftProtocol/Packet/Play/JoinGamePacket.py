#!/usr/bin/env python

from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection
from ...StreamIO import StreamIO


class JoinGamePacket(BasePacket):
    PACKET_ID = 0x23
    PACKET_DIRECTION = PacketDirection.CLIENTBOUND

    def __init__(self, entity_id, gamemode, dimension, difficulty, max_players, level_type, debug_info):
        BasePacket.__init__(self)
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

    @staticmethod
    def write(stream, packet):
        StreamIO.write_int(stream, packet.entity_id)
        StreamIO.write_ubyte(stream, packet.gamemode)
        StreamIO.write_int(stream, packet.dimension)
        StreamIO.write_ubyte(stream, packet.difficulty)
        StreamIO.write_ubyte(stream, packet.max_players)
        StreamIO.write_string(stream, packet.level_type.encode("utf8"))
        StreamIO.write_boolean(stream, packet.debug_info)

    @staticmethod
    def read(stream, packet_size):
        entity_id = StreamIO.read_int(stream)
        gamemode = StreamIO.read_ubyte(stream)
        dimension = StreamIO.read_int(stream)
        difficulty = StreamIO.read_ubyte(stream)
        max_players = StreamIO.read_ubyte(stream)
        level_type = StreamIO.read_string(stream).decode("utf8")
        debug_info = StreamIO.read_bool(stream)

        return JoinGamePacket(entity_id, gamemode, dimension, difficulty, max_players, level_type, debug_info)
