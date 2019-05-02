#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 2:17 PM
# author: liteng

import struct

from src.bottom.wallet import keytool
from src.bottom.tx.outpoint import OutPoint


class Input(object):
    def __init__(self, outpoint=None, sequence=0):
        if outpoint is None:
            self.previous = OutPoint()
        else:
            self.previous = outpoint
        self.sequence = sequence

    def deserialize(self, f):
        self.previous.deserialize(f)
        self.sequence = struct.unpack("<I", f.read(4))[0]

    def serialize(self):
        r = b""
        r += self.previous.serialize()
        r += struct.pack("<I", self.sequence)
        return r

    def __repr__(self):
        return "Input(previous=%s sequence=%i)" % (repr(self.previous), self.sequence)


if __name__ == '__main__':
    hash = keytool.sha256_hash(bytes("hello".encode("utf-8")), 2)
    index = 21

    op = OutPoint(hash.hex(), index)
    print(op)
    serial = op.serialize()

    input = Input(op, 100)
    input_serial = input.serialize()
    print("input: ", input)
    print("serial : ", serial.hex())
    print("input s: ", input_serial.hex())
