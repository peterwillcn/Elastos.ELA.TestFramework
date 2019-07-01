#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 10:53 AM
# author: liteng

import struct

MAX_UINT_16 = (1 << 16) - 1
MAX_UINT_32 = (1 << 32) - 1

PUSH_BYTES_75 = 0x4b
PUSH_DATA1 = 0x4c
PUSH_DATA2 = 0x4d
PUSH_DATA4 = 0x4e
PUSH_M1 = 0x4f
PUSH_0 = 0x00
PUSH_1 = 0x51


def write_var_uint(var: int):
    r = b""
    if var < 0xfd:
        r += struct.pack("<B", var)
        return r

    if var <= MAX_UINT_16:
        r += struct.pack("<B", 0xfd)
        r += struct.pack("<H", var)
        return r

    if var <= MAX_UINT_32:
        r += struct.pack("<B", 0xfe)
        r += struct.pack("<L", var)
        return r

    r += struct.pack("<B", 0xff)
    r += struct.pack("<Q", var)

    return r


def write_var_bytes(r: bytes, var: bytes):
    r += write_var_uint(len(var))
    r += var
    return r


def write_neo_bool(data: bool):
    if data:
        r = struct.pack("<B", PUSH_1)
    else:
        r = struct.pack("<B", PUSH_0)

    return r


def write_neo_integer(data: int):

    if data == -1:
        r = struct.pack("<B", PUSH_M1)
    elif data == 0:
        r = struct.pack("<B", PUSH_0)
    elif data < 16:
        r = struct.pack("<B", PUSH_1 - 1 + data)
    else:
        data_bytes = data.to_bytes(8, byteorder="little", signed=False)
        r = write_neo_bytes(data_bytes)

    return r


def write_neo_bytes(var: bytes):
    r = b""
    l = len(var)
    if l < PUSH_BYTES_75:
        r += struct.pack("<B", l)
    elif l < 0x100:
        r += struct.pack("<B", PUSH_DATA1)
        r += struct.pack("<B", l)
    elif l < 0x10000:
        r += struct.pack("<B", PUSH_DATA2)
        r += struct.pack("<H", l)
    else:
        r += struct.pack("<B", PUSH_DATA4)
        r += struct.pack("<I", l)

    r += var

    return r


if __name__ == '__main__':

    print("max uint 16: ", MAX_UINT_16)
    print("max uint 16: ", MAX_UINT_32)


