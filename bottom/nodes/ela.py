#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 5:30 PM
# author: liteng

from middle.common import constant
from bottom.nodes.node import Node


class MainNode(Node):

    def __init__(self, config, index: int, node_public_key):
        Node.__init__(self, config)
        self.tag = "[bottom.nodes.mainnode.MainNode]"
        self.index = index
        self.node_public_key = node_public_key

    def reset_config(self, num: int, update_content: dict):
        Node.reset_config_common(self, self.index, "ela", num)

        self.config[constant.CONFIG_FOUNDATION_ADDRESS] = update_content["foundation_address"]
        self.config[constant.CONFIG_POW][constant.CONFIG_PAY_TO_MINER] = update_content["miner_address"]
        self.config[constant.CONFIG_POW][constant.CONFIG_AUTO_MINING] = update_content["auto_mining"]
        self.config[constant.CONFIG_POW][constant.CONFIG_INSTANT_BLOCK] = update_content["instant_block"]
        self.config[constant.CONFIG_CHECK_ADDRESS_HEIGHT] = update_content["heights"][0]
        self.config[constant.CONFIG_VOTE_START_HEIGHT] = update_content["heights"][1]
        self.config[constant.CONFIG_ONLY_DPOS_HEIGHT] = update_content["heights"][2]
        self.config[constant.CONFIG_PUBLIC_DPOS_HEIGHT] = update_content["heights"][3]

        self.config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PORT_NODE] = self.reset_port(
            self.index,
            "ela",
            "arbiter_node_port"
        )
        self.config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PUBLIC_KEY] = self.node_public_key

        crc_number = len(update_content["crc_public_keys"])
        self.config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_CRC_ARBITERS] = self.get_crc_config(
            crc_public_keys=update_content["crc_public_keys"]
        )
        self.config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_NORMAL_ARBITERS_COUNT] = crc_number * 2
        self.config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_CANDIDATES_COUNT] = crc_number * 6
        self.config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PRE_CONNECT_OFFSET] = \
                                                                update_content["pre_connect_offset"]

    def start(self):
        pass

    def get_crc_config(self, crc_public_keys: list):
        crc_arbiters = list()
        for index in range(len(crc_public_keys)):
            crc_element = dict()
            print("crc public key: ", crc_public_keys[index], "index = ", index)
            crc_element[constant.CONFIG_PUBLIC_KEY] = crc_public_keys[index]
            crc_element[constant.CONFIG_NET_ADDRESS] = "127.0.0.1:" \
                                                       + str(Node.reset_port(self, index, "ela", "arbiter_node_port"))
            crc_arbiters.append(crc_element)
        return crc_arbiters
