#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:28
# file: node.py

import os
import subprocess
from utils import switch
from utils import util
from logs.log import Logger
from configs import constant


class Node(object):

    def __init__(self, index: int, node_type: str, cwd_dir, config, content):
        self.tag = '[Node]'
        self.index = index
        self.node_type = node_type
        self.cwd_dir = cwd_dir
        self.config = config
        self.content = content
        # print("configuration: ", self.config)
        self.configuration = self.config[constant.CONFIG_TITLE]
        self.process = None
        self.running = False
        self.switch_node = switch.switch_node_type()
        self.info_port = 0
        self.rest_port = 0
        self.ws_port = 0
        self.rpc_port = 0
        self.node_port = 0
        self.open_port = 0
        self.dev_null = open(os.devnull, 'w')
        self.switch_port = switch.switch_port_type()
        self.switch_bianry = switch.switch_binary()
        self.binary = self.switch_bianry[self.node_type]
        self.main_chain_foundation_address = content[constant.MAIN_CHAIN_FOUNDATION_ADDRESS]
        self.side_chain_foundation_address = content[constant.SIDE_CHAIN_FOUNDATION_ADDRESS]
        self.miner_address = content[constant.MINER_ADDRESS]

        self._reset_ports()

    def _reset_ports(self,):
        self.info_port = util.reset_config_ports(self.index, self.node_type, constant.CONFIG_PORT_INFO)
        self.rest_port = util.reset_config_ports(self.index, self.node_type, constant.CONFIG_PORT_REST)
        self.ws_port = util.reset_config_ports(self.index, self.node_type, constant.CONFIG_PORT_WS)
        self.rpc_port = util.reset_config_ports(self.index, self.node_type, constant.CONFIG_PORT_JSON)
        self.node_port = util.reset_config_ports(self.index, self.node_type, constant.CONFIG_PORT_NODE)
        self.open_port = util.reset_config_ports(self.index, self.node_type, constant.CONFIG_PORT_OPEN)

    def start(self):
        self.process = subprocess.Popen('./' + self.binary, stdout=self.dev_null,
                                        shell=True, cwd=self.cwd_dir)
        self.running = True
        Logger.debug('{} {} {} started on success.'.format(self.tag, self.binary, self.index))

    def stop(self):
        if not self.running:
            Logger.error('{} {} {} has already stopped'.format(
                            self.tag, self.binary, self.index))
            return
        try:
            self.process.terminate()
        except subprocess.SubprocessError as e:
            Logger.error('{} Unable to stop {} {}, error: {}'.format(
                self.tag, self.binary, self.index, e))
        self.running = False
        Logger.debug('{} {} {} has stopped successfully!'.format(self.tag, self.binary, self.index))

    def generate_config(self):
        self.configuration[constant.CONFIG_PORT_INFO] = self.info_port
        self.configuration[constant.CONFIG_PORT_REST] = self.rest_port
        self.configuration[constant.CONFIG_PORT_WS] = self.ws_port
        self.configuration[constant.CONFIG_PORT_JSON] = self.rpc_port
        self.configuration[constant.CONFIG_PORT_NODE] = self.node_port
        self.configuration[constant.CONFIG_PORT_OPEN] = self.open_port


class MainNode(Node):

    def __init__(self, index, cwd_dir, config, content):
        Node.__init__(self, index, constant.NODE_TYPE_MAIN, cwd_dir, config, content)
        self.tag = '[MainNode]'

    def generate_config(self):
        Node.generate_config(self)
        self.configuration[constant.CONFIG_FOUNDATION_ADDRESS] = self.main_chain_foundation_address
        self.configuration[constant.CONFIG_POW][constant.CONFIG_PAY_TO_MINER] = self.miner_address
        self.configuration[constant.CONFIG_ARBITERS] = self.content[constant.CONFIG_ARBITERS]
        return self.config


class ArbiterNode(Node):

    def __init__(self, index, cwd_dir, config, content):
        self.tag = '[ArbiterNode]'
        Node.__init__(self, index, constant.NODE_TYPE_ARBITER, cwd_dir, config, content)

    def generate_config(self):
        Node.generate_config(self)
        self.configuration["MainNode"]["Rpc"]["HttpJsonPort"] = util.reset_config_ports(self.index,
                                                                constant.NODE_TYPE_MAIN, constant.CONFIG_PORT_JSON)
        self.configuration["MainNode"]["DefaultPort"] = self.content[constant.MAIN_CHAIN_DEFAULT_PORT]
        self.configuration["MainNode"]["FoundationAddress"] = self.main_chain_foundation_address
        self.configuration["MainNode"]["SpvSeedList"] = self.content[constant.SPV_SEED_LIST]

        self.configuration['SideNodeList'][0]["Rpc"]["HttpJsonPort"] = util.reset_config_ports(self.index,
                                                                constant.NODE_TYPE_DID, constant.CONFIG_PORT_JSON)
        self.configuration['SideNodeList'][0]['PayToAddr'] = self.miner_address


class DidNode(Node):

    def __init__(self, index, cwd_dir, config, content):
        self.tag = '[DidNode]'
        Node.__init__(self, index, constant.NODE_TYPE_DID, cwd_dir, config, content)

    def generate_config(self):
        Node.generate_config(self)

        self.configuration[constant.CONFIG_FOUNDATION_ADDRESS] = self.side_chain_foundation_address
        self.configuration[constant.MAIN_CHAIN_DEFAULT_PORT] = self.content[constant.MAIN_CHAIN_DEFAULT_PORT]
        self.configuration[constant.MAIN_CHAIN_FOUNDATION_ADDRESS] = self.main_chain_foundation_address
        self.configuration[constant.CONFIG_POW][constant.CONFIG_PAY_TO_MINER] = self.miner_address
        self.configuration[constant.SPV_SEED_LIST] = self.content[constant.SPV_SEED_LIST]


class TokenNode(Node):

    def __init__(self, index, cwd_dir, config, content):
        self.tag = '[TokenNode]'
        Node.__init__(self, index, constant.NODE_TYPE_TOKEN, cwd_dir, config, content)

    def generate_config(self):
        Node.generate_config(self)

        self.configuration[constant.CONFIG_FOUNDATION_ADDRESS] = self.side_chain_foundation_address
        self.configuration[constant.MAIN_CHAIN_DEFAULT_PORT] = self.content[constant.MAIN_CHAIN_DEFAULT_PORT]
        self.configuration[constant.MAIN_CHAIN_FOUNDATION_ADDRESS] = self.main_chain_foundation_address
        self.configuration[constant.CONFIG_POW][constant.CONFIG_PAY_TO_MINER] = self.miner_address
        self.configuration[constant.SPV_SEED_LIST] = self.content[constant.SPV_SEED_LIST]


class NeoNode(Node):

    def __init__(self, index, cwd_dir, config, content):
        self.tag = '[NeoNode]'
        Node.__init__(self, index, constant.NODE_TYPE_NEO, cwd_dir, config, content)

    def generate_config(self):
        Node.generate_config(self)

        self.configuration[constant.CONFIG_FOUNDATION_ADDRESS] = self.side_chain_foundation_address
        self.configuration[constant.MAIN_CHAIN_DEFAULT_PORT] = self.content[constant.MAIN_CHAIN_DEFAULT_PORT]
        self.configuration[constant.MAIN_CHAIN_FOUNDATION_ADDRESS] = self.main_chain_foundation_address
        self.configuration[constant.CONFIG_POW][constant.CONFIG_PAY_TO_MINER] = self.miner_address
        self.configuration[constant.SPV_SEED_LIST] = self.content[constant.SPV_SEED_LIST]


