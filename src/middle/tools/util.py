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


def assert_equal(arg1, arg2):
    result = False
    if arg1 != arg2:
        print(constant.COLOR_RED + "[NOT EQUAL]" + constant.COLOR_END)
        # exit(-1)
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


