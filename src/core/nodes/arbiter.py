#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 5:59 PM
# author: liteng

import os
import time
import subprocess

from src.tools import util, constant
from src.tools.log import Logger
from src.core.managers.keystore_manager import KeyStoreManager

from src.core.nodes.node import Node
from src.core.parameters.arbiter_params import ArbiterParams


class ArbiterNode(Node):

    def __init__(self, index, config, params: ArbiterParams, keystore_manager: KeyStoreManager, cwd_dir: str):
        Node.__init__(self, config)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.index = index
        self.params = params
        self.keystore_manager = keystore_manager
        self.cwd_dir = cwd_dir
        self.rpc_port = self.reset_port(index, "arbiter", "json_port")
        self.err_output = open(os.path.join(self.cwd_dir, "error.log"), 'w')

        self.process = None
        self.running = False

    def start(self):
        self.process = subprocess.Popen(
            "./arbiter{} -p {}".format(self.index, self.params.password),
            stdout=self.dev_null,
            stderr=self.err_output,
            shell=True,
            cwd=self.cwd_dir
        )
        time.sleep(0.2)
        self.running = True
        Logger.debug("{} ./arbiter{} started on success.".format(self.tag, self.index))
        return True

    def stop(self):
        if not self.running:
            Logger.error("{} arbiter{} has already stopped".format(self.tag, self.index))
            return
        try:
            self.process.terminate()
            self.dev_null.close()
            self.err_output.close()
        except subprocess.SubprocessError as e:
            Logger.error("{} Unable to stop ela{}, error: {}".format(self.tag, self.index, e))
        self.running = False
        Logger.debug("{} arbiter{} has stopped on success!".format(self.tag, self.index))

    def reset_config(self):

        Node.reset_config_common(self, self.index, "arbiter", self.params.number)
        _config = self.config[constant.CONFIG_TITLE]
        _config[constant.CONFIG_MAGIC] = self.params.magic
        _config[constant.CONFIG_ACTIVE_NET] = self.params.active_net
        _config[constant.CONFIG_PRINT_LEVEL] = self.params.print_level
        _config[constant.CONFIG_SPV_PRINT_LEVEL] = self.params.spv_print_level
        _config[constant.CONFIG_ARBITER_MAIN_NODE] = self.gen_main_node()
        _config[constant.CONFIG_SIDE_NODE_LIST] = self.gen_side_node_list()
        _config[constant.CONFIG_ORIGIN_CROSS_CHAIN_ARBITERS] = self.gen_arbiters_list(0, 5)
        _config[constant.CONFIG_CRC_CROSS_CHAIN_ARBITERS] = self.gen_arbiters_list(5, 5 + self.params.crc_number)
        _config[constant.CONFIG_CRC_ONLY_DPOS_HEIGHT] = self.params.crc_dpos_only_height

        if self.index > 4:
            index = self.index % 5 + 1
        else:
            index = self.index
        _config[constant.CONFIG_DPOS_NET_ADDRESS] = "127.0.0.1:" + str(self.reset_port(
            index=index,
            node_type="ela",
            port_type="arbiter_node_port"
        ))

    def gen_main_node(self):
        main_node = dict()
        main_node[constant.CONFIG_ARBITER_RPC] = dict()
        rpc_config = main_node[constant.CONFIG_ARBITER_RPC]
        rpc_config[constant.CONFIG_ARBITER_IP_ADDRESS] = "127.0.0.1"
        if self.index > 4:
            index = self.index % 5 + 1
        else:
            index = self.index
        rpc_config[constant.CONFIG_PORT_JSON] = self.reset_port(
            index=index,
            node_type="ela",
            port_type="json_port"
        )
        rpc_config[constant.CONFIG_RPC_USER] = ""
        rpc_config[constant.CONFIG_RPC_PASS] = ""
        rpc_config[constant.CONFIG_RPC_WHITE_LIST] = ["0.0.0.0"]
        main_node[constant.CONFIG_SPV_SEED_LIST] = list()
        main_node[constant.CONFIG_SPV_SEED_LIST].append("127.0.0.1:" + str(self.reset_port(
            index=index,
            node_type="ela",
            port_type="node_port"
        )))
        main_node[constant.CONFIG_MAGIC] = self.params.spv_magic
        main_node[constant.CONFIG_MIN_OUTBOUND] = 1
        main_node[constant.CONFIG_MAX_CONNECTION] = 3
        main_node[constant.CONFIG_FOUNDATION_ADDRESS] = self.keystore_manager.special_key_stores[0].address
        main_node[constant.CONFIG_PORT_ARBITER_MAIN_DEFAULT] = self.reset_port(
            index=index,
            node_type="ela",
            port_type="node_port"
        )
        return main_node

    def gen_side_node_list(self):
        side_node_list = list()

        for side_node in self.params.side_info.keys():
            side_dict = dict()
            side_dict[constant.CONFIG_ARBITER_RPC] = dict()

            rpc_config = side_dict[constant.CONFIG_ARBITER_RPC]
            rpc_config[constant.CONFIG_ARBITER_IP_ADDRESS] = "127.0.0.1"
            rpc_config[constant.CONFIG_PORT_JSON] = self.reset_port(
                index=self.index % 5,
                node_type=side_node,
                port_type="json_port"
            )
            rpc_config[constant.CONFIG_RPC_USER] = ""
            rpc_config[constant.CONFIG_RPC_PASS] = ""

            side_dict[constant.CONFIG_EXCHANGE_RATE] = 1.0
            side_dict[constant.CONFIG_GENESIS_BLOCK] = self.params.side_info[side_node][constant.SIDE_GENESIS_ADDRESS]

            if side_node is "did":
                side_dict[constant.CONFIG_MINER_ADDRESS] = self.keystore_manager.sub_key_stores[self.index].address
            elif side_node is "token":
                side_dict[constant.CONFIG_MINER_ADDRESS] = self.keystore_manager.sub_key_stores2[self.index].address
            side_dict[constant.CONFIG_PAY_TO_ADDR] = self.keystore_manager.special_key_stores[3].address
            side_dict[constant.CONFIG_POW_CHAIN] = self.params.pow_chain

            side_node_list.append(side_dict)

        return side_node_list

    def gen_arbiters_list(self, start: int, end: int):
        arbiters_list = list()
        for i in range(start, end):
            arbiters_list.append(self.keystore_manager.arbiter_stores[i].public_key.hex())

        return arbiters_list
