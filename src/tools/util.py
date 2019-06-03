#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-17 10:20
# file: common.py

import os
import json
import struct

from src.tools.log import Logger

PROJECT_NAME = "Elastos.ELA.TestFramework"

node_type_dict = {
    "ela": 10,
    "arbiter": 20,
    "did": 30,
    "token": 40,
    "neo": 50
}


port_type_dict = {
    "info_port": 3,
    "rest_port": 4,
    "ws_port": 5,
    "json_port": 6,
    "node_port": 8,
    "arbiter_node_port": 9
}

TO_SELA = 100000000
TX_FEE = 10000


def reset_port(index, node_type: str, port_type: str):
    port = (100 + index) * 100 + node_type_dict[node_type] + port_type_dict[port_type]
    return port


def get_go_path():
    go_path = ""
    path = os.environ.get("GOPATH")
    if ":" in path:
        go_path = path.split(":")[0]
    return go_path


def tag_from_path(path: str, class_name: str):
    elements = path.split("/")
    index = elements.index(PROJECT_NAME)
    tag = "["
    for i in range(index + 1, len(elements)):
        if i == len(elements) - 1:
            tag += elements[i].split(".")[0]
            if class_name is not "":
                tag += "."
                tag += class_name
            break
        tag += elements[i]
        tag += "."
    tag += "]"
    return tag


def arbiter_public_keys(key_stores):
    public_keys = []
    if len(key_stores) != 5:
        Logger.error("[common] Invalid argument, the length of the argument must be equal 5")
        exit(0)
    for key_store in key_stores:
        public_keys.append(key_store.public_key.hex())
    return public_keys


def assert_equal(send_resp, jar_txid):
    result = False
    if send_resp != jar_txid:
        print("jar_txid: {}".format(jar_txid))
        print("send_res: {}".format(send_resp))
        print(Logger.COLOR_RED + "[NOT EQUAL]" + Logger.COLOR_END)
    else:
        result = True
    return result


def read_config_file(config_file_path):
    with open(config_file_path, "r", encoding="utf8") as f:
        content = f.read()
        # print("content: ", content, "content type: ", type(content))
        if content.startswith(u"\ufeff"):
            content = content.encode("utf8")[3:].decode("utf8")
        load_dict = json.loads(content)

    return load_dict


def write_config_file(config_dict, config_file_path):
    with open(config_file_path, "w", encoding="utf8") as f:
        json.dump(config_dict, f, indent=4)


def save_to_json(k, prefix: str, dest_path: str, first_time: bool):

    if os.path.exists(dest_path) and not first_time:
        with open(dest_path, "r") as f:
            load_dict = json.load(f)
            load_dict[prefix] = k.to_dict()
        with open(dest_path, "w", buffering=1) as f:
            json.dump(load_dict, f, indent=4)
    else:
        with open(dest_path, "w", buffering=1) as f:
            json.dump({prefix: k.to_dict()}, f, indent=4)


def save_to_dat(keystore_dat: dict, dat_file_path: str):
    with open(dat_file_path, "w", buffering=1) as f:
        json.dump(keystore_dat, f, sort_keys=False, indent=4, separators=(',', ':'))


def deser_uint256(f):
    r = 0
    for i in range(8):
        t = struct.unpack("<I", f.read(4))[0]
        r += t << (i * 32)
    return r


def ser_uint256(u):
    rs = b""
    for i in range(8):
        rs += struct.pack("<I", u & 0xFFFFFFFF)
        u >>= 32
    return rs


def bytes_reverse(u: bytes):
    return u[::-1]

