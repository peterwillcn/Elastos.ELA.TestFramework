#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/20 3:37 PM
# author: liteng

import os
import json
import time
import shutil

from configs import constant
from configs import config
from decimal import Decimal
from logs.log import Logger
from utils import switch
from utils import util
from core.deploy import node
from core.service.jar import JarService
from core.service.rpc import RPC
from core.service.rest import REST
from core.wallet import keystoremanager


class Deploy(object):

    def __init__(self, jar_service: JarService, rpc: RPC, rest: REST, key_stores: list):
        self.tag = '[Deploy] '
        self._jar_service = jar_service
        self._rpc = rpc
        self._rest = rest
        self._key_stores = key_stores
        self.main_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []
        self.switch_list = self._switch_list()
        self.switch_path = switch.switch_path()
        self.switch_config = switch.switch_config()
        self.main_chain_foundation_address = self._key_stores[0].address
        self.side_chain_foundation_address = self._key_stores[1].address
        self.miner_address = self._key_stores[2].address
        self.arbiter_public_keys = util.gen_arbiter_public_keys(self._key_stores[3:8])

    def _switch_list(self):
        switcher = {
            constant.NODE_TYPE_MAIN: self.main_nodes,
            constant.NODE_TYPE_ARBITER: self.arbiter_nodes,
            constant.NODE_TYPE_DID: self.did_nodes,
            constant.NODE_TYPE_TOKEN: self.token_nodes,
            constant.NODE_TYPE_NEO: self.neo_nodes
        }
        return switcher

    def _switch_node(self, index, cmd_dir, _config, content):
        switcher = {
            constant.NODE_TYPE_MAIN: node.MainNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_ARBITER: node.ArbiterNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_DID: node.DidNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_TOKEN: node.TokenNode(index, cmd_dir, _config, content),
            constant.NODE_TYPE_NEO: node.NeoNode(index, cmd_dir, _config, content)
        }
        return switcher

    def deploy_nodes(self):

        # if num < 0:
        #     Logger.error('{} Invalid param num: {}'.format(self.tag, num))
        #     return False
        # Logger.debug('{} deploy {} binary'.format(self.tag, node_type))
        node_type = constant.NODE_TYPE_MAIN
        src_path = os.path.join(self.switch_path[node_type])
        if not os.path.exists(src_path):
            Logger.error('{} path not found: '.format(src_path))
            return False
        _config = self.switch_config[node_type]

        content = {}
        content[constant.MAIN_CHAIN_FOUNDATION_ADDRESS] = self.main_chain_foundation_address
        content[constant.SIDE_CHAIN_FOUNDATION_ADDRESS] = self.side_chain_foundation_address
        content[constant.MINER_ADDRESS] = self.miner_address

        for i in range(constant.NODE_INIT_NUMBER_MAIN):
            dest_path = os.path.join(constant.TEST_PARAENT_PATH, node_type,
                                     constant.CURRENT_DATE_TIME, 'node' + str(i))
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            shutil.copy(src_path, dest_path + '/ela')

            config_path = os.path.join(dest_path, 'config.json')
            # config_path = dest_path + '/config.json'
            main_chain_default_port = util.reset_config_ports(i, constant.NODE_TYPE_MAIN, constant.CONFIG_PORT_OPEN)
            content[constant.MAIN_CHAIN_DEFAULT_PORT] = main_chain_default_port
            content[constant.SPV_SEED_LIST] = [constant.HOST_NAME + ':' + str(main_chain_default_port)]
            content[constant.CONFIG_ARBITERS] = self.arbiter_public_keys
            n = self._switch_node(i, dest_path, _config, content)[node_type]
            n.generate_config()
            with open(config_path, 'w') as f:
                json.dump(n.config, f, indent=4)
            self.switch_list[node_type].append(n)

        return True

    def start_nodes(self):
        length = len(self.main_nodes)
        for i in range(length):
            self.main_nodes[i].start()
            time.sleep(1)

        self._wait_rpc_service()
        time.sleep(2)
        self._rpc.discrete_mining(101)
        balance = self._rpc.get_balance_by_address(self.main_chain_foundation_address)
        Logger.debug('{} foundation address balance: {}'.format(self.tag, balance))

    def stop_nodes(self):
        length = len(self.main_nodes)
        for i in range(length):
            self.main_nodes[i].stop()
        self._jar_service.stop()

    def _wait_rpc_service(self, content=1,  timeout=60):

        stop_time = time.time() + timeout

        while time.time() <= stop_time:
            result = []
            for i in range(len(self.main_nodes)):
                count = self._rpc.get_connection_count()
                Logger.debug('{} connection count: {}'.format(self.tag, count))
                if count and count >= content:
                    result.append(True)
                else:
                    result.append(False)
                if result.count(True) == len(self.main_nodes):
                    Logger.debug('{} Nodes connect with each other, '
                                 'rpc service is successfully started.'.format(self.tag))
                    return True
                time.sleep(2)
        Logger.error('{} Node can not connect with each other, wait rpc service timed out!')
        return False


