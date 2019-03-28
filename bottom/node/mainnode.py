#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 5:30 PM
# author: liteng

from bottom.node.node import Node


class MainNode(Node):

    def __init__(self, config, index: int):
        Node.__init__(self)
        self.config = config
        self.index = index
        pass

    def reset_config(self):
        pass

    def start(self):
        pass