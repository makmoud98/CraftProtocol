from distutils.core import setup
from CraftProtocol.VersionConstants import VersionConstants

setup(
	name = "CraftProtocol",
	packages = [
		"CraftProtocol",
		"CraftProtocol.NBT",
		"CraftProtocol.Packet",
		"CraftProtocol.Packet.Handshaking",
		"CraftProtocol.Packet.Status",
		"CraftProtocol.Packet.Login",
		"CraftProtocol.Packet.Play",
		"CraftProtocol.Client",
		"CraftProtocol.Client.Event"
	],
	version = VersionConstants.VERSION,
	description = "Open source partial implementation of Minecraft network protocol (currently only 1.10.x) and NBT in Python 2.7. Also easy-to-use library for creating bots.",
	author = "Toranktto",
	python_requires = "~=2.7",
	license = "MIT",
	author_email = "toranktto@gmail.com",
	url = "https://github.com/Toranktto/CraftProtocol",
	classifiers = []
)