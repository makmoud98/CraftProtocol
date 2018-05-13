#!/usr/bin/env python

import CraftProtocol
import socket
import json
import time

HOSTNAME = "localhost"
PORT = 25565

def main():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.settimeout(5)
	sock.connect((HOSTNAME, PORT))

	start_time = time.time()

	serializer = CraftProtocol.Packet.PacketSerializer(CraftProtocol.Packet.PacketDirection.SERVERBOUND)

	handshake = CraftProtocol.Packet.Handshaking.HandshakePacket(CraftProtocol.ProtocolVersion.MC_1_10, HOSTNAME, PORT, CraftProtocol.ProtocolState.STATUS)
	request = CraftProtocol.Packet.Status.RequestPacket()

	serializer.write(sock, handshake)
	serializer.set_state(CraftProtocol.ProtocolState.STATUS)
	serializer.write(sock, request)

	response = serializer.read(sock)

	if not isinstance(response, CraftProtocol.Packet.Status.ResponsePacket):
		print "Invalid packet received"
		sock.close()
		return

	json_response = json.loads(response.get_json())

	delta_time = time.time() - start_time

	print "Server description:\n"
	print CraftProtocol.ChatSerializer.strip_colors(json_response["description"])
	print ""
	print "Time: %.2f ms" % (delta_time)

	sock.close()

if __name__ == "__main__": main()