#!/usr/bin/env python
import CraftProtocol
import gzip
import urllib2

EXPECTED_VALUE = "Compound tag #1"

def main():
	print "Downloading bigtest.nbt..."
	connection = urllib2.urlopen("https://raw.github.com/Dav1dde/nbd/master/test/bigtest.nbt")
	data = connection.read()
	f = open("bigtest.nbt", "wb")
	f.write(data)
	f.close()
	print "Downloaded!"

	with gzip.open("bigtest.nbt", "rb") as f:
		tag = CraftProtocol.NBT.NBTSerializer.read(f)
		value = tag["listTest (compound)"][1]["name"].get()
		if value == EXPECTED_VALUE:
			print "Test OK!"
		else:
			print "Test FAILED!"
			print "Expected value = " + EXPECTED_VALUE
			print "Real value = " + value

if __name__ == "__main__": main()