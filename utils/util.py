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


def post_request(method, port: int, params):
    try:
        url = 'http://127.0.0.1:' + str(port)
        resp = requests.post(url, json={"method": method, "params": params},
                                 headers={"content-type": "application/json"})
        response = resp.json()
        if response[constant.POST_RESPONSE_ERROR] == None:
            return response[constant.POST_RESPONSE_RESULT]
        else:
            return response[constant.POST_RESPONSE_ERROR]
    except requests.exceptions.RequestException as e:
        return False

