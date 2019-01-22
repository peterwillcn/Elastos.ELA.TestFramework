#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/21 9:27 PM
# author: liteng

from configs import constant
from configs import config


def switch_path():
    switcher = {
        constant.NODE_TYPE_MAIN: constant.NODE_PATH_MAIN,
        constant.NODE_TYPE_ARBITER: constant.NODE_PATH_ARBITER,
        constant.NODE_TYPE_DID: constant.NODE_PATH_DID,
        constant.NODE_TYPE_TOKEN: constant.NODE_PATH_TOKEN,
        constant.NODE_TYPE_NEO: constant.NODE_PATH_NEO
    }
    return switcher


def switch_config():
    switcher = {
        constant.NODE_TYPE_MAIN: config.main_chain,
        constant.NODE_TYPE_ARBITER: config.arbiter_chain,
        constant.NODE_TYPE_DID: config.did_chain,
        constant.NODE_TYPE_TOKEN: config.token_chain,
        constant.NODE_TYPE_NEO: config.neo_chain
    }
    return switcher


def switch_node_type():
    switcher = {
        constant.NODE_TYPE_MAIN: 10,
        constant.NODE_TYPE_ARBITER: 20,
        constant.NODE_TYPE_DID: 30,
        constant.NODE_TYPE_TOKEN: 40,
        constant.NODE_TYPE_NEO: 50
        }
    return switcher


def switch_port_type():
    switcher = {
        constant.CONFIG_PORT_INFO: 1,
        constant.CONFIG_PORT_REST: 2,
        constant.CONFIG_PORT_WS: 3,
        constant.CONFIG_PORT_JSON: 4,
        constant.CONFIG_PORT_NODE: 5,
        constant.CONFIG_PORT_OPEN: 6
    }
    return switcher


def switch_binary():
    switcher = {
        constant.NODE_TYPE_MAIN: constant.NODE_BINARY_MAIN,
        constant.NODE_TYPE_ARBITER: constant.NODE_BINARY_ARBITER,
        constant.NODE_TYPE_DID: constant.NODE_BINARY_DID,
        constant.NODE_TYPE_TOKEN: constant.NODE_BINARY_TOKEN,
        constant.NODE_TYPE_NEO: constant.NODE_BINARY_NEO
    }
    return switcher