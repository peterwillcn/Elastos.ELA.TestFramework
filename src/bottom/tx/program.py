#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 11:12 AM
# author: liteng

from src.bottom.tx import serialize


class Program(object):

    def __init__(self, code=None, params=None):
        self.code = code
        self.parameter = params

    def serialize(self):
        r = b""
        r = serialize.write_var_bytes(r, self.parameter)
        r = serialize.write_var_bytes(r, self.code)

        return r

    def deserialize(self):
        pass

    def __repr__(self):
        return "Program: {\n\t" + "code: " + self.code.hex() + "\n\t" + "parameter: " + self.parameter.hex() + "\n}"


