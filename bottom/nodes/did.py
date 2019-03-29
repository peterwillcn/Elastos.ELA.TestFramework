#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:01 PM
# author: liteng

from bottom.nodes.node import Node


class Did(Node):

    def __init__(self, config, index: int):
        Node.__init__(self, config)
        self.tag = "[bottom.nodes.did.Did]"
        self.index = index

    def reset_config(self, num: int):
        Node.reset_config_common(self, self.index, "did", num)