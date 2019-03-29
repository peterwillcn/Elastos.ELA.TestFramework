#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 5:30 PM
# author: liteng

from middle import util
from middle import constant
from bottom.nodes.node import Node


class MainNode(Node):

    def __init__(self, config, index: int):
        Node.__init__(self, config)
        self.tag = "[bottom.nodes.mainnode.MainNode]"
        self.index = index

    def reset_config(self, num: int):
        Node.reset_config_common(self, self.index, "ela", num)
        self.config[constant.CONFIG_ARBITER_CONFIGURATION][constant.CONFIG_PORT_NODE] = self.reset_port(
            self.index,
            "ela",
            "arbiter_node_port"
        )

    def start(self):
        pass