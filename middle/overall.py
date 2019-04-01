#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 2:48 PM
# author: liteng

import time

from middle.common.log import Logger
from middle.parameters.params import Parameter

from bottom.nodes.node_manager import NodeManager
from bottom.services.rpc import RPC


class Overall(object):

    def __init__(self, top_config, project_root_path: str):
        self.tag = "[middle.overall.Overall]"
        self.params = Parameter(top_config)
        self.rpc = RPC()
        self.node_manager = NodeManager(self.rpc, self.params, project_root_path)

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
        ret = False
        if self.params.ela_params.enable:
            ret = self.node_manager.start_nodes()
        time.sleep(4)
        self.rpc.discrete_mining(101)
        Logger.debug("{} mining 101 blocks on success!".format(self.tag))
        foundation_value = self.rpc.get_balance_by_address(self.params.ela_params.foundation_address)
        Logger.debug("{} The value of foundation address is {}".format(self.tag, foundation_value))
        return ret

    def stop_node(self):
        if self.params.ela_params.enable:
            self.node_manager.stop_nodes()


