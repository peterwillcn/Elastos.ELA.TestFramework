#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:02 PM
# author: liteng

from bottom.node.node import Node


class Neo(Node):

    def __init__(self, config, index):
        Node.__init__(self)
        self.config = config
        self.index = index

    def reset_config(self):
        pass
