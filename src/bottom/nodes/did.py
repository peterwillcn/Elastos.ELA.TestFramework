#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:01 PM
# author: liteng

import subprocess

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger
from src.middle.managers.keystore_manager import KeyStoreManager

from src.bottom.nodes.node import Node
from src.bottom.parameters.did_params import DidParams


class DidNode(Node):

    def __init__(self, index, config, params: DidParams, keystore_manager: KeyStoreManager, cwd_dir: str):
        Node.__init__(self, config)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.index = index
        self.params = params
        self.keystore_manager = keystore_manager
        self.cwd_dir = cwd_dir
        self.rpc_port = self.reset_port(index, "did", "json_port")
        self.process = None
        self.running = False

    def start(self):
        self.process = subprocess.Popen('./did{} 2>output'.format(self.index), stdout=self.dev_null, shell=True, cwd=self.cwd_dir)
        self.running = True
        Logger.debug('{} ./did{} started on success.'.format(self.tag, self.index))
        return True

    def stop(self):
        if not self.running:
            Logger.error('{} did{} has already stopped'.format(self.tag, self.index))
            return
        try:
            self.process.terminate()
        except subprocess.SubprocessError as e:
            Logger.error('{} Unable to stop ela{}, error: {}'.format(self.tag, self.index, e))
        self.running = False
        Logger.debug('{} did{} has stopped on success!'.format(self.tag, self.index))

    def reset_config(self):
        Node.reset_config_common(self, self.index, "did", self.params.number)
        _config = self.config[constant.CONFIG_TITLE]
        _config[constant.CONFIG_MAGIC] = self.params.magic
        _config[constant.CONFIG_SPV_MAGIC] = self.params.spv_magic
        _config[constant.CONFIG_SPV_SEED_LIST] = self.gen_spv_seed_list()
        _config[constant.CONFIG_MAIN_CHAIN_FOUNDATION_ADDRESS] = self.keystore_manager.special_key_stores[0].address
        _config[constant.CONFIG_FOUNDATION_ADDRESS] = self.keystore_manager.special_key_stores[1].address
        _config[constant.CONFIG_POW][constant.CONFIG_PAY_TO_ADDR] = self.keystore_manager.special_key_stores[3].address
        _config[constant.CONFIG_POW][constant.CONFIG_INSTANT_BLOCK] = self.params.instant_block
        _config[constant.CONFIG_PORT_MAIN_CHAIN_DEFAULT] = self.reset_port(
            index=self.index,
            node_type="ela",
            port_type="node_port"
        )

    def gen_spv_seed_list(self):
        spv_seed_list = list()
        for i in range(self.params.number):
            spv_seed_list.append("127.0.0.1:" + str(self.reset_port(
                index=i,
                node_type="ela",
                port_type="node_port"
            )))
        return spv_seed_list

