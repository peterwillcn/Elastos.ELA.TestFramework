#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 2:48 PM
# author: liteng

from middle.nodemanager import NodeManager
from middle.params import Parameter


class Overall(object):

    def __init__(self, top_config):
        self.params = Parameter(top_config)
        self.node_manager = NodeManager()
        pass

    def deploy_node(self):
        if self.params.ela_node_enable:
            self.node_manager.deploy_node("ela",  self.params.ela_node_num)
        if self.params.arbiter_node_enable:
            self.node_manager.deploy_node("arbiter", self.params.arbiter_node_num)
        if self.params.did_node_enable:
            self.node_manager.deploy_node("did", self.params.did_node_num)
        if self.params.token_node_enable:
            self.node_manager.deploy_node("token", self.params.token_node_num)
        if self.params.neo_node_enable:
            self.node_manager.deploy_node("neo", self.params.neo_node_num)

    def start_node(self):
        pass

    def stop_node(self):
        pass
