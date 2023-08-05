# Copyright (c) 2012-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

import ctypes as ct
from memorybuffer import Py_buffer, Buffer, isbuffer


class ByteBuffer(Buffer):

  # byte_buffer, readonly = ct.create_string_buffer(b"ABCDEFGHIJ"), True
    byte_buffer, readonly = bytearray(b"ABCDEFGHIJ"), False

    raw_bytes = (ct.c_ubyte * len(byte_buffer)).from_buffer(byte_buffer)

    # Buffer protocol

    def __getbuffer__(self, buffer, flags):

        length   = len(self.raw_bytes) - 1
        itemsize = 1

        buffer.buf        = ct.cast(self.raw_bytes, ct.c_void_p)
        buffer.len        = length * itemsize
        buffer.itemsize   = itemsize
        buffer.readonly   = self.readonly
        buffer.format     = b"b"
        buffer.ndim       = 1
        buffer.shape      = (ct.c_ssize_t * 1)(length)
        buffer.strides    = (ct.c_ssize_t * 1)(itemsize)
        buffer.suboffsets = None
        buffer.obj        = ct.py_object(self)

        self.__buffer_exports__ = getattr(self,"__buffer_exports__",0) + 1

    def __releasebuffer__(self, buffer):

        if self.__buffer_exports__ > 0:
            self.__buffer_exports__ -= 1

        if self.__buffer_exports__ != 0 or not buffer.buf:
            return

        buffer.buf = None


def main():

    buf = ByteBuffer()

    print()
    print("Is buffer: {}".format(isbuffer(buf)))
    print()

    mem = memoryview(buf)
    print(chr(mem[0]), chr(mem[1]), chr(mem[2]))
    for b in mem:
        print(chr(b), end=" ")
    print()
    print()

    mem[0] = ord("X")
    mem[5] = ord("Z")
    print(chr(mem[0]), chr(mem[1]), chr(mem[2]))
    for b in mem:
        print(chr(b), end=" ")
    print()


main()
