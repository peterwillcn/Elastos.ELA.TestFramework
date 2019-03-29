#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:02 PM
# author: liteng

from bottom.nodes.node import Node


class Neo(Node):

    def __init__(self, config, index):
        Node.__init__(self, config)
        self.tag = "[bottom.nodes.neo.Neo]"
        self.index = index

    def reset_config(self, num: int):
        Node.reset_config_common(self, self.index, "neo", num)
