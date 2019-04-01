#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 4:59 PM
# author: liteng

import os
import time
import shutil

from middle.common import util
from middle.common.log import Logger
from middle.parameters.params import Parameter
from middle.common.env import Environment

from bottom.nodes.ela import ElaNode
from bottom.nodes.arbiter import Arbiter
from bottom.nodes.did import Did
from bottom.nodes.token import Token
from bottom.nodes.neo import Neo

from bottom.wallet.keystore_manager import KeyStoreManager


class NodeManager(object):

    def __init__(self, rpc, params: Parameter, project_root_path: str):
        self.tag = "[bottom.node.nodemanager.NodeManager]"
        self.ela_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []
        self.rpc = rpc
        self.params = params
        self.env = Environment(project_root_path)
        self.keystore_manager = KeyStoreManager(self.params.ela_params.number, self.params.ela_params.password)

        self.nodes_dict = {
            "ela": self.ela_nodes,
            "arbiter": self.arbiter_nodes,
            "did": self.did_nodes,
            "token": self.token_nodes,
            "neo": self.neo_nodes
        }

    def update_ela_config(self, update_content: dict):
        update_content["crc_public_keys"] = list()
        for i in range(self.params.ela_params.crc_number):
            update_content["crc_public_keys"].append(self.keystore_manager.key_stores[i].public_key.hex())

        update_content["arbiter_enable"] = self.params.ela_params.arbiter_enable
        update_content["password"] = self.params.ela_params.password
        update_content["auto_mining"] = self.params.ela_params.auto_mining
        update_content["instant_block"] = self.params.ela_params.instant_block
        update_content["foundation_address"] = self.params.ela_params.foundation_address
        update_content["miner_address"] = self.params.ela_params.miner_address
        update_content["pre_connect_offset"] = self.params.ela_params.pre_connect_offset
        update_content["heights"] = list()
        update_content["heights"].append(self.params.ela_params.check_address_height)
        update_content["heights"].append(self.params.ela_params.vote_start_height)
        update_content["heights"].append(self.params.ela_params.crc_dpos_height)
        update_content["heights"].append(self.params.ela_params.public_dpos_height)

    @staticmethod
    def init_node(category: str, config, index: int, node_public_key, cwd_dir: str):

        if category == "ela":
            node = ElaNode(config, index, node_public_key, cwd_dir)
        elif category == "arbiter":
            node = Arbiter(config, index, cwd_dir)
        elif category == "did":
            node = Did(config, index, cwd_dir)
        elif category == "token":
            node = Token(config, index, cwd_dir)
        elif category == "neo":
            node = Neo(config, index, cwd_dir)
        else:
            node = None

        return node

    def deploy_node(self, category: str, num: int, config_update_content: dict):
        src_path = os.path.join(self.env.elastos_path, self.env.src_path_dict[category])
        if not os.path.exists(src_path):
            return False
        Logger.debug("{} src_path: {}".format(self.tag, src_path))
        config_path = os.path.join(src_path, "config.json.sample")
        if os.path.exists(config_path):
            Logger.debug("{} config.json will generate from the sample".format(self.tag))
            config_dict = util.read_config_file(config_path)
        else:
            Logger.debug("{} config.json will generate from the default".format(self.tag))
            config_dict = self.env.config_dict[category]

        self.update_ela_config(config_update_content["ela"])

        for i in range(num):
            dest_path = os.path.join(self.env.test_path, category + "_nodes", self.env.current_date_time,
                                     category + str(i))
            Logger.debug("{} dest_path: {}".format(self.tag, dest_path))
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            shutil.copy(os.path.join(src_path, category), os.path.join(dest_path, category))
            node = self.init_node(category, config_dict, i,
                                  self.keystore_manager.key_stores[i].public_key.hex(), dest_path)
            node.reset_config(num, config_update_content[category])
            util.write_config_file(node.config, os.path.join(dest_path, "config.json"))
            self.nodes_dict[category].append(node)

            if category == "ela":
                shutil.copy(
                    os.path.join(self.env.project_root_path, "bottom/datas/general", "keystore_" + str(i) + ".dat"),
                    os.path.join(dest_path, "keystore.dat")
                )

            if i == 0 and category == "ela":
                shutil.copy(
                    os.path.join(self.env.project_root_path, "bottom/datas/special/foundation.dat"),
                    os.path.join(os.path.join(dest_path, "foundation.dat"))
                )

                shutil.copy(
                    os.path.join(self.env.project_root_path, "bottom/datas/special/miner.dat"),
                    os.path.join(os.path.join(dest_path, "miner.dat"))
                )

        return True

    def start_nodes(self):
        for i in range(len(self.ela_nodes)):
            self.ela_nodes[i].start()
            time.sleep(1)
        ret = self._wait_rpc_service()
        return ret

    def stop_nodes(self):
        for i in range(len(self.ela_nodes)):
            self.ela_nodes[i].stop()
            time.sleep(0.5)

    def _wait_rpc_service(self, content=1,  timeout=60):

        stop_time = time.time() + timeout
        while time.time() <= stop_time:
            result = []
            for i in range(len(self.ela_nodes)):
                count = self.rpc.get_connection_count()
                Logger.debug('{} connection count: {}'.format(self.tag, count))
                if count and count >= content:
                    result.append(True)
                else:
                    result.append(False)
                if result.count(True) == len(self.ela_nodes):
                    Logger.debug('{} Nodes connect with each other, '
                                 'rpc service is started on success!.'.format(self.tag))
                    return True
                time.sleep(2)
        Logger.error('{} Node can not connect with each other, wait rpc service timed out!')
        return False



