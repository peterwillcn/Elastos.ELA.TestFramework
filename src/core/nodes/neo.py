#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:02 PM
# author: liteng

import os
import subprocess

from src.tools import util, constant
from src.tools.log import Logger

from src.core.nodes.node import Node
from src.core.parameters.neo_params import NeoParams
from src.core.managers.keystore_manager import KeyStoreManager


class NeoNode(Node):

    def __init__(self, index, config, params: NeoParams, keystore_manager: KeyStoreManager, cwd_dir):
        Node.__init__(self, config)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.index = index
        self.params = params
        self.keystore_manager = keystore_manager
        self.cwd_dir = cwd_dir
        self.rpc_port = self.reset_port(index, "neo", "json_port")
        self.err_output = open(os.path.join(self.cwd_dir, "error.log"), 'w')
        self.process = None
        self.running = None

    def start(self):
        self.process = subprocess.Popen(
            "./neo{}".format(self.index),
            stdout=self.dev_null,
            stderr=self.err_output,
            shell=True,
            cwd=self.cwd_dir
        )
        self.running = True
        Logger.debug("{} ./neo{} started on success.".format(self.tag, self.index))
        return True

    def stop(self):
        if not self.running:
            Logger.error("{} neo{} has already stopped".format(self.tag, self.index))
            return
        try:
            self.process.terminate()
            self.dev_null.close()
            self.err_output.close()
        except subprocess.SubprocessError as e:
            Logger.error("{} Unable to stop neo{}, error: {}".format(self.tag, self.index, e))
        self.running = False
        Logger.debug("{} neo{} has stopped on success!".format(self.tag, self.index))

    def reset_config(self):
        Node.reset_config_common(self, self.index, "neo", self.params.number)
        _config = self.config
        _config[constant.CONFIG_ACTIVE_NET] = self.params.active_net
        _config[constant.CONFIG_MAGIC] = self.params.magic
        _config[constant.CONFIG_PORT_NODE] = self.reset_port(
            index=self.index,
            node_type="neo",
            port_type="node_port"
        )

        _config[constant.CONFIG_SPV_MAGIC] = self.params.spv_magic
        _config[constant.CONFIG_DISABLE_DNS] = self.params.disable_dns
        _config[constant.CONFIG_PERMANENT_PEERS] = self.gen_permanent_list()
        _config[constant.CONFIG_SIDE_SPV_DISABLE_DNS] = self.params.spv_disable_dns
        _config[constant.CONFIG_SIDE_SPV_PERMANENT_PEERS] = self.gen_spv_permanent_list()
        _config[constant.CONFIG_SIDE_ENABLE_REST] = self.params.rest_port_enable
        _config[constant.CONFIG_SIDE_PORT_REST] = self.reset_port(
            index=self.index,
            node_type="neo",
            port_type="rest_port"
        )
        _config[constant.CONFIG_SIDE_ENABLE_WS] = self.params.ws_port_enable
        _config[constant.CONFIG_SIDE_PORT_WS] = self.reset_port(
            index=self.index,
            node_type="neo",
            port_type="ws_port"
        )

        _config[constant.CONFIG_SIDE_ENABLE_RPC] = self.params.rpc_port_enable
        _config[constant.CONFIG_SIDE_PORT_RPC] = self.reset_port(
            index=self.index,
            node_type="neo",
            port_type="json_port"
        )

        _config[constant.CONFIG_SIDE_RPC_USER] = ""
        _config[constant.CONFIG_SIDE_RPC_PASS] = ""
        _config[constant.CONFIG_SIDE_RPC_WHITE_LIST] = ["0.0.0.0"]
        _config[constant.CONFIG_SIDE_LOG_LEVEL] = self.params.log_level
        _config[constant.CONFIG_SIDE_ENABLE_MINING] = self.params.mining_enable
        _config[constant.CONFIG_INSTANT_BLOCK] = self.params.instant_block
        _config[constant.CONFIG_PAY_TO_ADDR] = self.keystore_manager.side_miner_account.address()

        _config[constant.CONFIG_FOUNDATION_ADDRESS] = self.keystore_manager.foundation_account.address()

    def gen_spv_permanent_list(self):
        spv_seed_list = list()
        for i in range(self.params.number + 1):
            if i == 0:
                continue
            spv_seed_list.append("127.0.0.1:" + str(self.reset_port(
                index=i,
                node_type="ela",
                port_type="node_port"
            )))
        return spv_seed_list

    def gen_permanent_list(self):
        permanent_list = list()
        for i in range(self.params.number + 1):
            if i == 0:
                continue
            permanent_list.append("127.0.0.1:" + str(self.reset_port(
                index=i,
                node_type="neo",
                port_type="node_port"
            )))

        return permanent_list