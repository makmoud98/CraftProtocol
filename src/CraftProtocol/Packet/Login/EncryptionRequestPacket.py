#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class EncryptionRequestPacket(BasePacket):

	PACKET_ID = 0x01
	PACKET_DIRECTION = PacketDirection.CLIENTBOUND

	def __init__(self, server_id, public_key, verify_token):
		BasePacket.__init__(self)
		self.server_id = server_id
		self.public_key = public_key
		self.verify_token = verify_token

	def get_server_id(self):
		return self.server_id

	def get_public_key(self):
		return self.public_key

	def get_verify_token(self):
		return self.verify_token

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.server_id.encode("utf8"))
		StreamIO.write_string(stream, packet.public_key)
		StreamIO.write_string(stream, packet.verify_token)

	@staticmethod
	def read(stream, packet_size):
		server_id = StreamIO.read_string(stream).decode("utf8")
		public_key = StreamIO.read_string(stream)
		verify_token = StreamIO.read_string(stream)

		return EncryptionRequestPacket(server_id, public_key, verify_token)