#!/usr/bin/env python

from ...StreamIO import StreamIO
from ..BasePacket import BasePacket
from ..PacketDirection import PacketDirection

class EncryptionResponsePacket(BasePacket):

	PACKET_ID = 0x01
	PACKET_DIRECTION = PacketDirection.SERVERBOUND

	def __init__(self, shared_secret, verify_token):
		BasePacket.__init__(self)
		self.shared_secret = shared_secret
		self.verify_token = verify_token

	def get_shared_secret(self):
		return self.shared_secret

	def get_verify_token(self):
		return self.verify_token

	@staticmethod
	def write(stream, packet):
		StreamIO.write_string(stream, packet.shared_secret)
		StreamIO.write_string(stream, packet.verify_token)

	@staticmethod
	def read(stream, packet_size):
		shared_secret = StreamIO.read_string(stream)
		verify_token = StreamIO.read_string(stream)

		return EncryptionRequestPacket(shared_secret, verify_token)