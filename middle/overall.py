#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 2:48 PM
# author: liteng

from bottom.nodes.nodemanager import NodeManager
from middle.params import Parameter


class Overall(object):

    def __init__(self, top_config):
        self.tag = "[middle.overall.Overall]"
        self.params = Parameter(top_config)
        self.check_params()
        self.node_manager = NodeManager(self.params)

        pass

    def deploy_node(self):
        ret = False
        if self.params.ela_node_enable:
            ret = self.node_manager.deploy_node("ela",  self.params.ela_node_num)
        if self.params.arbiter_node_enable:
            ret = self.node_manager.deploy_node("arbiter", self.params.arbiter_node_num)
        if self.params.did_node_enable:
            ret = self.node_manager.deploy_node("did", self.params.did_node_num)
        if self.params.token_node_enable:
            ret = self.node_manager.deploy_node("token", self.params.token_node_num)
        if self.params.neo_node_enable:
            ret = self.node_manager.deploy_node("neo", self.params.neo_node_num)
        return ret

    def start_node(self):
        pass

    def stop_node(self):
        pass

    def check_params(self):
        if self.params.ela_node_num < self.params.crc_number:
            print("{} Ela should have more nodes than crc, please check your config.json file...".format(self.tag))
            exit(-1)
        else:
            print("{} Parameters Check Pass!".format(self.tag))
