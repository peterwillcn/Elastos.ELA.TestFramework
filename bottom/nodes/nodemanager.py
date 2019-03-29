#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 4:59 PM
# author: liteng

import os
import shutil

from middle import util
from middle.params import Parameter
from middle.env import Environment

from bottom.nodes.mainnode import MainNode
from bottom.nodes.arbiter import Arbiter
from bottom.nodes.did import Did
from bottom.nodes.token import Token
from bottom.nodes.neo import Neo

from bottom.wallet.keystoremanager import KeyStoreManager


class NodeManager(object):

    def __init__(self, params: Parameter):
        self.tag = "[bottom.node.nodemanager.NodeManager]"
        self.ela_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []
        self.params = params
        self.env = Environment()
        self.keystore_manager = KeyStoreManager(self.params.ela_node_num, self.params.password)

        self.nodes_dict = {
            "ela": self.ela_nodes,
            "arbiter": self.arbiter_nodes,
            "did": self.did_nodes,
            "token": self.token_nodes,
            "neo": self.neo_nodes
        }

    def deploy_node(self, category: str, num: int):
        src_path = os.path.join(self.env.elastos_path, self.env.src_path_dict[category])
        if not os.path.exists(src_path):
            return False
        print("src_path: ", src_path)
        config_path = os.path.join(src_path, "config.json.sample")
        if os.path.exists(config_path):
            config_dict = util.read_config_file(config_path)
        else:
            config_dict = self.env.config_dict[category]

        config_update_content = dict()
        config_update_content["crc_public_keys"] = list()
        for i in range(self.params.crc_number):
            config_update_content["crc_public_keys"].append(self.keystore_manager.key_stores[i].public_key.hex())

        config_update_content["pre_connect_offset"] = self.params.pre_connect_offset
        config_update_content["heights"] = list()
        config_update_content["heights"].append(self.params.check_address_height)
        config_update_content["heights"].append(self.params.vote_start_height)
        config_update_content["heights"].append(self.params.crc_only_dpos_height)
        config_update_content["heights"].append(self.params.public_dpos_height)


        for i in range(num):
            dest_path = os.path.join(self.env.test_path, category + "_nodes", self.env.current_date_time,
                                     category + str(i))
            print("dest_path: ", dest_path)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            shutil.copy(os.path.join(src_path, category), os.path.join(dest_path, category))
            node = self.init_node(category, config_dict, i, self.keystore_manager.key_stores[i].public_key.hex())
            node.reset_config(num, config_update_content)
            util.write_config_file(node.config, os.path.join(dest_path, "config.json"))
            self.nodes_dict[category].append(node)

            if category == "ela":
                shutil.copy(os.path.join(
                    self.env.project_root_path, "bottom/datas/keystores", "keystore_" + str(i) + ".dat"),
                    os.path.join(dest_path, "keystore.dat"))

        return True

    @staticmethod
    def init_node(category: str, config, index: int, node_public_key):

        if category == "ela":
            node = MainNode(config, index, node_public_key)
        elif category == "arbiter":
            node = Arbiter(config, index)
        elif category == "did":
            node = Did(config, index)
        elif category == "token":
            node = Token(config, index)
        elif category == "neo":
            node = Neo(config, index)
        else:
            node = None

        return node

