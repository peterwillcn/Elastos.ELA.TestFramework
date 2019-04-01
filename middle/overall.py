#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 2:48 PM
# author: liteng

from bottom.nodes.node_manager import NodeManager
from middle.parameters.params import Parameter


class Overall(object):

    def __init__(self, top_config):
        self.tag = "[middle.overall.Overall]"
        self.params = Parameter(top_config)
        self.node_manager = NodeManager(self.params)

        pass

    def deploy_node(self):
        ret = False

        config_update_content = dict()
        config_update_content["ela"] = dict()
        config_update_content["arbiter"] = dict()
        config_update_content["did"] = dict()
        config_update_content["token"] = dict()
        config_update_content["neo"] = dict()

        if self.params.ela_params.enable:
            ret = self.node_manager.deploy_node("ela",  self.params.ela_params.number, config_update_content)
        if self.params.arbiter_params.enable:
            ret = self.node_manager.deploy_node("arbiter", self.params.arbiter_params.number, config_update_content)
        if self.params.did_params.enable:
            ret = self.node_manager.deploy_node("did", self.params.did_params.number, config_update_content)
        if self.params.token_params.enable:
            ret = self.node_manager.deploy_node("token", self.params.token_params.number, config_update_content)
        if self.params.neo_params.enable:
            ret = self.node_manager.deploy_node("neo", self.params.neo_params.number, config_update_content)
        return ret

    def start_node(self):
        pass

    def stop_node(self):
        pass


