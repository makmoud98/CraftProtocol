#!/usr/bin/env python

import struct


class StreamIO(object):

    @staticmethod
    def write_bool(stream, x):
        if x:
            StreamIO.write_ubyte(stream, 0x01)
        else:
            StreamIO.write_ubyte(stream, 0x00)

    @staticmethod
    def read_bool(stream):
        x = StreamIO.read_ubyte(stream)
        if x == 0x01:
            return True

        return False

    @staticmethod
    def write_byte(stream, x):
        StreamIO.write(stream, struct.pack("b", x))

    @staticmethod
    def read_byte(stream):
        return struct.unpack("b", StreamIO.read(stream, 1))[0]

    @staticmethod
    def write_ubyte(stream, x):
        StreamIO.write(stream, struct.pack("B", x))

    @staticmethod
    def read_ubyte(stream):
        return struct.unpack("B", StreamIO.read(stream, 1))[0]

    @staticmethod
    def write_varint(stream, x):
        if x < 0:
            x = (1 << 32) + x

        buf = ""
        while True:
            byte = x & 0x7f
            x >>= 7
            if x:
                buf += chr(byte | 0x80)
            else:
                buf += chr(byte)
                break

        StreamIO.write(stream, buf)

    @staticmethod
    def read_varint(stream):
        shift = 0
        result = 0
        while True:
            i = StreamIO.read_byte(stream)
            result |= (i & 0x7F) << shift
            shift += 7
            if not (i & 0x80):
                break

        if result & (1 << 31):
            result = result - (1 << 32)

        return result

    @staticmethod
    def size_varint(x):
        if x < 0:
            x = (1 << 32) + x

        size = 1
        while x & ~0x7f:
            size += 1
            x >>= 7
        return size

    write_varlong = write_varint
    read_varlong = read_varint
    size_varlong = size_varint

    @staticmethod
    def write_ushort(stream, x):
        StreamIO.write(stream, struct.pack("!H", x))

    @staticmethod
    def read_ushort(stream):
        return struct.unpack("!H", StreamIO.read(stream, 2))[0]

    @staticmethod
    def write_short(stream, x):
        StreamIO.write(stream, struct.pack("!h", x))

    @staticmethod
    def read_short(stream):
        raw = StreamIO.read(stream, 2)
        return struct.unpack("!h", raw)[0]

    @staticmethod
    def write_int(stream, x):
        StreamIO.write(stream, struct.pack("!i", x))

    @staticmethod
    def read_int(stream):
        return struct.unpack("!i", StreamIO.read(stream, 4))[0]

    @staticmethod
    def write_long(stream, x):
        StreamIO.write(stream, struct.pack("!q", x))

    @staticmethod
    def read_long(stream):
        return struct.unpack("!q", StreamIO.read(stream, 8))[0]

    @staticmethod
    def write_ulong(stream, x):
        StreamIO.write(stream, struct.pack("!Q", x))

    @staticmethod
    def read_ulong(stream):
        return struct.unpack("!Q", StreamIO.read(stream, 8))[0]

    @staticmethod
    def write_float(stream, x):
        StreamIO.write(stream, struct.pack("!f", x))

    @staticmethod
    def read_float(stream):
        return struct.unpack("!f", StreamIO.read(stream, 4))[0]

    @staticmethod
    def write_double(stream, x):
        StreamIO.write(stream, struct.pack("!d", x))

    @staticmethod
    def read_double(stream):
        return struct.unpack("!d", StreamIO.read(stream, 8))[0]

    @staticmethod
    def write_string(stream, x):
        StreamIO.write_varint(stream, len(x))
        StreamIO.write(stream, x)

    @staticmethod
    def read_string(stream):
        return StreamIO.read(stream, StreamIO.read_varint(stream))

    @staticmethod
    def write(stream, data):
        if hasattr(stream, "send") and callable(stream.send):
            return stream.send(data)

        return stream.write(data)

    @staticmethod
    def read(stream, n):
        if hasattr(stream, "recv") and callable(stream.recv):
            data = stream.recv(n)
            while len(data) < n:
                packet = stream.recv(n - len(data))
                if not packet:
                    stream.close()
                    raise EOFError("Unexpected EOF while reading bytes")

                data += packet

            return data

        data = stream.read(n)
        if len(data) < n:
            raise EOFError("Unexpected EOF while reading bytes")

        return data
