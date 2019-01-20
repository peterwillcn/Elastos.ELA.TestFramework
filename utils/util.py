#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-17 10:20
# file: util.py

from configs import constant


def encode_point(is_compressed, ecc_publick_key):
    public_key_x = ecc_publick_key._point._x
    public_key_y = ecc_publick_key._point._y

    if public_key_x is None or public_key_y is None:
        infinity = []
        for i in range(constant.INFINITY_LEN):
            infinity.append(constant.EMPTY_BYTE)
        return infinity
    encoded_data = []
    if is_compressed:
        for i in range(constant.COMPRESSED_LEN):
            encoded_data.append(constant.EMPTY_BYTE)
    else:
        for i in range(constant.NON_COMPRESSED_LEN):
            encoded_data.append(constant.EMPTY_BYTE)
        y_bytes = public_key_y.to_bytes()
        for i in range(constant.NON_COMPRESSED_LEN - len(y_bytes), constant.NON_COMPRESSED_LEN):
            encoded_data[i] = y_bytes[i - constant.NON_COMPRESSED_LEN + len(y_bytes)]

    x_bytes = public_key_x.to_bytes()
    x_len = len(x_bytes)
    for i in range(constant.COMPRESSED_LEN - x_len, constant.COMPRESSED_LEN):
        encoded_data[i] = x_bytes[i - constant.COMPRESSED_LEN + x_len]

    if is_compressed:
        if public_key_y % 2 == 0:
            encoded_data[0] = constant.COMPEVEN_FLAG
        else:
            encoded_data[0] = constant.COMPODD_FLAG
    else:
        encoded_data[0] = constant.NON_COMPRESSED_FLAG
    return bytes(encoded_data)



