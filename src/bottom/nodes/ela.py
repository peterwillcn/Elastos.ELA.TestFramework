#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 5:30 PM
# author: liteng

import os
import subprocess

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger

from src.middle.managers.keystore_manager import KeyStoreManager

from src.bottom.nodes.node import Node
from src.bottom.parameters.ela_params import ElaParams


class ElaNode(Node):

    def __init__(self, index: int, config, params: ElaParams, keystore_manager: KeyStoreManager, cwd_dir: str):
        Node.__init__(self, config)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.index = index
        self.params = params
        self.keystore_manager = keystore_manager
        self.owner_keystore = keystore_manager.owner_key_stores[index]
        self.node_keystore = keystore_manager.node_key_stores[index]
        self.cwd_dir = cwd_dir
        self.password = self.params.password
        self.rpc_port = self.reset_port(self.index, "ela", "json_port")
        self.err_output = open(os.path.join(self.cwd_dir, "error.log"), 'w')

        self.process = None
        self.running = False

    def reset_config(self):
        Node.reset_config_common(self, self.index, "ela", self.params.number)

        _config = self.config[constant.CONFIG_TITLE]
        if self.index == 0:
            _config[constant.CONFIG_ARBITER_ENABLE] = False
        else:
            _config[constant.CONFIG_ARBITER_ENABLE] = self.params.arbiter_enable

        _config[constant.CONFIG_MAGIC] = self.params.magic
        _config[constant.CONFIG_PRINT_LEVEL] = self.params.print_level
        _config[constant.CONFIG_FOUNDATION_ADDRESS] = self.keystore_manager.special_key_stores[0].address
        _config[constant.CONFIG_POW][constant.CONFIG_PAY_TO_ADDR] = self.keystore_manager.special_key_stores[1].address
        _config[constant.CONFIG_POW][constant.CONFIG_AUTO_MINING] = self.params.auto_mining
        _config[constant.CONFIG_POW][constant.CONFIG_INSTANT_BLOCK] = self.params.instant_block
        _config[constant.CONFIG_CHECK_ADDRESS_HEIGHT] = self.params.check_address_height
        _config[constant.CONFIG_VOTE_START_HEIGHT] = self.params.vote_start_height
        _config[constant.CONFIG_ONLY_DPOS_HEIGHT] = self.params.crc_dpos_height
        _config[constant.CONFIG_PUBLIC_DPOS_HEIGHT] = self.params.public_dpos_height
        # rpc accept set

        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PUBLIC_KEY] = self.node_keystore.public_key.hex()
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PORT_NODE] = self.reset_port(
            self.index,
            "ela",
            "arbiter_node_port"
        )
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_IP_ADDRESS] = self.params.ip_address
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PRINT_LEVEL] = self.params.print_level
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_ORIGIN_ARBITERS] = self.gen_original_arbiter()
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_CRC_ARBITERS] = self.gen_crc_config()
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_NORMAL_ARBITERS_COUNT] = \
            self.params.crc_number * 2
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_EMERGENCY_INACTIVE_PENALTY] = \
                                                                        self.params.emergency_inactive_penalty
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_INACTIVE_PENALTY] = self.params.inactive_penalty
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_CANDIDATES_COUNT] = self.params.crc_number * 6
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PRE_CONNECT_OFFSET] = \
            self.params.pre_connect_offset
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_MAX_INACTIVATE_ROUNDS] = \
            self.params.max_inactivate_rounds

    def start(self):
        if self.params.arbiter_enable and self.index != 0:
            self.process = subprocess.Popen(
                "./ela{} -p {}".format(self.index, self.password),
                stdout=self.dev_null,
                stderr=self.err_output,
                shell=True,
                cwd=self.cwd_dir
            )
            if self.index in range(1, self.params.crc_number + 1):
                Logger.debug("{} crc{} started on success.".format(self.tag, self.index))
            elif self.index in range(self.params.crc_number + 1, self.params.crc_number * 3 + 1):
                Logger.debug("{} producer{} started on success.".format(self.tag, self.index))
            else:
                Logger.debug("{} candidate{} started on success.".format(self.tag, self.index))
        else:
            self.process = subprocess.Popen(
                "./ela{}".format(self.index),
                stdout=self.dev_null,
                stderr=self.err_output,
                shell=True,
                cwd=self.cwd_dir
            )
            if self.index == 0:
                Logger.debug("{} miner started on success.".format(self.tag))
            else:
                Logger.debug("{} normal ela{} started on success.".format(self.tag, self.index))

        self.running = True
        return True

    def stop(self):
        if not self.running:
            Logger.error("{} ela{} has already stopped".format(self.tag, self.index))
            return
        try:
            self.process.terminate()
            self.dev_null.close()
            self.err_output.close()
        except subprocess.SubprocessError as e:
            Logger.error("{} Unable to stop ela{}, error: {}".format(self.tag, self.index, e))
        self.running = False
        Logger.debug("{} ela{} has stopped on success!".format(self.tag, self.index))

    def gen_crc_config(self):
        crc_arbiters = list()
        for index in range(1, self.params.crc_number + 1):
            crc_element = dict()
            crc_element[constant.CONFIG_PUBLIC_KEY] = self.keystore_manager.node_key_stores[index].public_key.hex()
            crc_element[constant.CONFIG_NET_ADDRESS] = "127.0.0.1:" \
                                                       + str(Node.reset_port(self, index, "ela", "arbiter_node_port"))
            crc_arbiters.append(crc_element)
        return crc_arbiters

    def gen_original_arbiter(self):
        origin_arbiters = []
        for keystore in self.keystore_manager.arbiter_stores[:5]:
            origin_arbiters.append(keystore.public_key.hex())
        return origin_arbiters
