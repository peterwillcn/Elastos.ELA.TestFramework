#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 5:30 PM
# author: liteng

import subprocess

from src.middle.common import constant
from src.middle.common.log import Logger

from src.bottom.nodes.node import Node


class ElaNode(Node):

    def __init__(self, config, index: int, owner_keystore, node_keystore, cwd_dir: str):
        Node.__init__(self, config)
        self.tag = "[src.bottom.nodes.ela.MainNode]"
        self.index = index
        self.owner_keystore = owner_keystore
        self.node_keystore = node_keystore
        self.cwd_dir = cwd_dir
        self.password = ""
        self.process = None
        self.running = False

    def reset_config(self, num: int, update_content: dict):
        Node.reset_config_common(self, self.index, "ela", num)
        self.password = update_content["password"]
        _config = self.config[constant.CONFIG_TITLE]
        _config[constant.CONFIG_ARBITER_ENABLE] = update_content["arbiter_enable"]
        _config[constant.CONFIG_FOUNDATION_ADDRESS] = update_content["foundation_address"]
        _config[constant.CONFIG_POW][constant.CONFIG_PAY_TO_MINER] = update_content["miner_address"]
        _config[constant.CONFIG_POW][constant.CONFIG_AUTO_MINING] = update_content["auto_mining"]
        _config[constant.CONFIG_POW][constant.CONFIG_INSTANT_BLOCK] = update_content["instant_block"]
        _config[constant.CONFIG_CHECK_ADDRESS_HEIGHT] = update_content["heights"][0]
        _config[constant.CONFIG_VOTE_START_HEIGHT] = update_content["heights"][1]
        _config[constant.CONFIG_ONLY_DPOS_HEIGHT] = update_content["heights"][2]
        _config[constant.CONFIG_PUBLIC_DPOS_HEIGHT] = update_content["heights"][3]

        # rpc accept set
        _config[constant.CONFIG_RPC][constant.CONFIG_RPC_USER] = ""
        _config[constant.CONFIG_RPC][constant.CONFIG_RPC_PASS] = ""
        _config[constant.CONFIG_RPC][constant.CONFIG_RPC_WHITE_LIST] = ["0.0.0.0"]
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PORT_NODE] = self.reset_port(
            self.index,
            "ela",
            "arbiter_node_port"
        )
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PUBLIC_KEY] = self.node_keystore.public_key.hex()

        crc_number = len(update_content["crc_public_keys"])
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_CRC_ARBITERS] = self.gen_crc_config(
            crc_public_keys=update_content["crc_public_keys"]
        )
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_NORMAL_ARBITERS_COUNT] = crc_number * 2
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_CANDIDATES_COUNT] = crc_number * 6
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PRE_CONNECT_OFFSET] = \
                                                                update_content["pre_connect_offset"]

    def start(self):
        self.process = subprocess.Popen('./ela -p ' + self.password, stdout=self.dev_null, shell=True, cwd=self.cwd_dir)
        self.running = True
        Logger.debug('{} ela{} -p {} started on success.'.format(self.tag, self.index, self.password))
        return True

    def stop(self):
        if not self.running:
            Logger.error('{} ela{} has already stopped'.format(self.tag, self.index))
            return
        try:
            self.process.terminate()
        except subprocess.SubprocessError as e:
            Logger.error('{} Unable to stop ela{}, error: {}'.format(self.tag, self.index, e))
        self.running = False
        Logger.debug('{} ela{} has stopped on success!'.format(self.tag, self.index))

    def gen_crc_config(self, crc_public_keys: list):
        crc_arbiters = list()
        for index in range(len(crc_public_keys)):
            crc_element = dict()
            crc_element[constant.CONFIG_PUBLIC_KEY] = crc_public_keys[index]
            crc_element[constant.CONFIG_NET_ADDRESS] = "127.0.0.1:" \
                                                       + str(Node.reset_port(self, index, "ela", "arbiter_node_port"))
            crc_arbiters.append(crc_element)
        return crc_arbiters
