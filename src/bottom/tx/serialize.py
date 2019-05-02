#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/2 10:53 AM
# author: liteng

import struct


def write_var_uint(var: int):
    if var < 0xfd:
        r = struct.pack("<B", var)
        return r


def write_var_bytes(r: bytes, var: bytes):
    r += write_var_uint(len(var))
    r += var
    return r


