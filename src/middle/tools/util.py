#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-17 10:20
# file: util.py

import os
import json
from src.middle.tools.log import Logger
from src.middle.tools import constant


node_type_dict = {
    "ela": 10,
    "arbiter": 20,
    "did": 30,
    "token": 40,
    "neo": 50
}


port_type_dict = {
    "info_port": 1,
    "rest_port": 2,
    "ws_port": 3,
    "json_port": 4,
    "node_port": 5,
    "arbiter_node_port": 6
}


def reset_port(index, node_type: str, port_type: str):
    port = (100 + index) * 100 + node_type_dict[node_type] + port_type_dict[port_type]
    return port


def get_go_path():
    go_path = ""
    path = os.environ.get("GOPATH")
    if ":" in path:
        go_path = path.split(":")[0]
    return go_path


def arbiter_public_keys(key_stores):
    public_keys = []
    if len(key_stores) != 5:
        Logger.error("[util] Invalid argument, the length of the argument must be equal 5")
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


def tag_from_path(path: str, class_name: str):
    elements = path.split("/")
    index = elements.index(constant.PROJECT_NAME)
    tag = "【"
    for i in range(index + 1, len(elements)):
        if i == len(elements) - 1:
            tag += elements[i].split(".")[0]
            if class_name is not "":
                tag += "."
                tag += class_name
            break
        tag += elements[i]
        tag += "."
    tag += "】"
    return tag


def read_config_file(config_file_path):
    with open(config_file_path, "r", encoding="utf8") as f:
        content = f.read()
        if content.startswith(u"\ufeff"):
            content = content.encode("utf8")[3:].decode("utf8")
        load_dict = json.loads(content)

    return load_dict


def write_config_file(config_dict, config_file_path):
    with open(config_file_path, "w", encoding="utf8") as f:
        json.dump(config_dict, f, indent=4)


