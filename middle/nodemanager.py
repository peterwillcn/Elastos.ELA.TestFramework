#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 4:59 PM
# author: liteng

import os
import shutil

from middle import util
from middle.env import Environment

from bottom.node.mainnode import MainNode
from bottom.node.arbiter import Arbiter
from bottom.node.did import Did
from bottom.node.token import Token
from bottom.node.neo import Neo


class NodeManager(object):

    def __init__(self):
        self.tag = "[middle.nodemanager.NodeManager]"
        self.ela_nodes = []
        self.arbiter_nodes = []
        self.did_nodes = []
        self.token_nodes = []
        self.neo_nodes = []
        self.env = Environment()

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

        for i in range(num):
            dest_path = os.path.join(self.env.test_path, category + "_nodes", self.env.current_date_time,
                                     category + str(i))
            print("dest_path: ", dest_path)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            shutil.copy(os.path.join(src_path, category), os.path.join(dest_path, category))
            node = self.init_node(category, config_dict, i)
            node.reset_config()
            util.write_config_file(node.config, os.path.join(dest_path, "config.json"))
            self.nodes_dict[category].append(node)

        return True

    @staticmethod
    def init_node(category: str, config, index: int):

        if category == "ela":
            node = MainNode(config, index)
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

