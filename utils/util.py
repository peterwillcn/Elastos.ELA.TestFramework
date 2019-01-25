#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-17 10:20
# file: util.py

import requests
from configs import constant
from utils import switch
from logs.log import Logger


def encode_point(is_compressed, ecc_publick_key):
    public_key_x = ecc_publick_key._point._x
    public_key_y = ecc_publick_key._point._y

    if public_key_x is None or public_key_y is None:
        infinity = []
        for i in range(1):
            infinity.append(0x00)
        return infinity
    encoded_data = []
    if is_compressed:
        for i in range(33):
            encoded_data.append(0x00)
    else:
        for i in range(65):
            encoded_data.append(0x00)
        y_bytes = public_key_y.to_bytes()
        for i in range(65 - len(y_bytes), 65):
            encoded_data[i] = y_bytes[i - 65 + len(y_bytes)]

    x_bytes = public_key_x.to_bytes()
    x_len = len(x_bytes)
    for i in range(33 - x_len, 33):
        encoded_data[i] = x_bytes[i - 33 + x_len]

    if is_compressed:
        if public_key_y % 2 == 0:
            encoded_data[0] = 0x02
        else:
            encoded_data[0] = 0x03
    else:
        encoded_data[0] = 0x04
    return bytes(encoded_data)


def reset_config_ports(index, node_type: str, port_type: str):
    port = (index + 100) * 100 + switch.switch_node_type()[node_type] + switch.switch_port_type()[port_type]
    return port


def gen_arbiter_public_keys(key_stores):
    public_keys = []
    if len(key_stores) != 5:
        Logger.error("[util] Invalid argument, the length of the argument must be equal 5")
        exit(0)
    for key_store in key_stores:
        public_keys.append(key_store.public_key.hex())
    return public_keys



