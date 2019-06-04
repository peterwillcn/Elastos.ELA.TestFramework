#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 5:30 PM
# author: liteng

import os
import subprocess

from src.tools import util, constant
from src.tools.log import Logger

from src.core.managers.keystore_manager import KeyStoreManager

from src.core.nodes.node import Node
from src.core.parameters.ela_params import ElaParams


class ElaNode(Node):

    TYPE_MINER = "miner"
    TYPE_CRC = "crc"
    TYPE_PRODUCER = "producer"
    TYPE_CANDIDATE = "candidate"
    TYPE_NORMAL = "normal"

    def __init__(self, index: int, config, params: ElaParams, keystore_manager: KeyStoreManager,
                 cwd_dir: str, ela_type: str):
        Node.__init__(self, config)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.index = index
        self.params = params
        self.keystore_manager = keystore_manager
        self.name = ""
        self.type = ela_type
        self.owner_account = keystore_manager.owner_accounts[self.index]
        self.node_account = keystore_manager.node_accounts[self.index]
        self.cwd_dir = cwd_dir
        self.password = self.params.password
        self.rpc_port = self.reset_port(self.index, "ela", "json_port")
        self.arbiter_node_port = self.reset_port(self.index, "ela", "arbiter_node_port")
        self.err_output = open(os.path.join(self.cwd_dir, "error.log"), 'w')
        self.arbiter_enable = False
        self.process = None
        self.running = False
        self.set_name()

    def set_name(self):
        if self.index == 0:
            self.name = "miner"
        elif self.index <= self.params.crc_number:
            self.name = "CRC-{0:03d}".format(self.index)
        elif self.index <= self.params.number - round(self.params.later_start_number / 2):
            self.name = "PRO-{0:03d}".format(self.index)
        else:
            self.name = "NOR-{0:03d}".format(self.index)

    def reset_config(self):
        Node.reset_config_common(self, self.index, "ela", self.params.number)

        _config = self.config[constant.CONFIG_TITLE]
        if self.index == 0 or self.params.later_start_number != 0 \
                and self.index >= self.params.number - int(self.params.later_start_number / 2) + 1:
            _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_ARBITER_ENABLE] = False
            self.arbiter_enable = False
        else:
            _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_ARBITER_ENABLE] = self.params.arbiter_enable
            self.arbiter_enable = self.params.arbiter_enable

        _config[constant.CONFIG_MAGIC] = self.params.magic
        _config[constant.CONFIG_PRINT_LEVEL] = self.params.print_level
        _config[constant.CONFIG_ACTIVE_NET] = self.params.active_net
        _config[constant.CONFIG_DISABLE_DNS] = self.params.disable_dns
        _config[constant.CONFIG_FOUNDATION_ADDRESS] = self.keystore_manager.foundation_account.address()
        _config[constant.CONFIG_POW][constant.CONFIG_PAY_TO_ADDR] = self.keystore_manager.main_miner_account.address()
        _config[constant.CONFIG_POW][constant.CONFIG_AUTO_MINING] = self.params.auto_mining
        _config[constant.CONFIG_POW][constant.CONFIG_INSTANT_BLOCK] = self.params.instant_block
        _config[constant.CONFIG_CHECK_ADDRESS_HEIGHT] = self.params.check_address_height
        _config[constant.CONFIG_VOTE_START_HEIGHT] = self.params.vote_start_height
        _config[constant.CONFIG_ONLY_DPOS_HEIGHT] = self.params.crc_dpos_height
        _config[constant.CONFIG_PUBLIC_DPOS_HEIGHT] = self.params.public_dpos_height
        # rpc accept set

        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PUBLIC_KEY] = self.node_account.public_key()
        _config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PORT_DPOS] = self.reset_port(
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
        if self.running:
            return
        if self.arbiter_enable:
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
            # self.dev_null.close()
            # self.err_output.close()
        except subprocess.SubprocessError as e:
            Logger.error("{} Unable to stop ela{}, error: {}".format(self.tag, self.index, e))
        self.running = False

    def gen_crc_config(self):
        crc_arbiters = list()
        for index in range(1, self.params.crc_number + 1):
            crc_arbiters.append(self.keystore_manager.node_accounts[index].public_key())
        return crc_arbiters

    def gen_original_arbiter(self):
        origin_arbiters = []
        for keystore in self.keystore_manager.origin_arbiter_accounts:
            origin_arbiters.append(keystore.public_key())
        return origin_arbiters

    def get_node_public_key(self):
        return self.node_account.public_key()

    def get_owner_public_key(self):
        return self.owner_account.public_key()

    def get_node_address(self):
        return self.node_account.address

    def get_owner_address(self):
        return self.owner_account.address

    def get_owner_private_key(self):
        return self.owner_account.private_key()


