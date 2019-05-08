#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 11:12 AM
# author: liteng

from src.tools import serialize


class Program(object):

    def __init__(self, code=None, params=None):
        self.code = code
        self.parameter = params

    def serialize(self):
        r = b""
        if self.parameter is None:
            r = serialize.write_var_bytes(r, bytes(0))
        else:
            r = serialize.write_var_bytes(r, self.parameter)
        if self.code is None:
            r = serialize.write_var_bytes(r, bytes(0))
        else:
            r = serialize.write_var_bytes(r, self.code)

        return r

    def deserialize(self):
        pass

    def __repr__(self):
        arg1 = ""
        arg2 = ""
        if self.code is not None:
            arg1 = self.code.hex()
        if self.parameter is not None:
            arg2 = self.parameter.hex()
        return "Program: {\n\t" + "code: " + arg1 + "\n\t" + "parameter: " + arg2 + "\n}"


if __name__ == '__main__':
    redeem_script = bytes.fromhex("2102d5b81d2f002b1ace56f6da5a35322df75544d71699af31bd30cfbfd348a61e15ac")
    program = Program(code=redeem_script, params=None)

    r = program.serialize()
    print("program serial: ", r.hex())

    a = b""
    b = bytes(0)
    c = a + b

    print("a = ", a)
    print("b = ", b)
    print("c = ", c)
