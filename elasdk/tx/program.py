#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 11:12 AM
# author: liteng

from elasdk.common import serialize


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



