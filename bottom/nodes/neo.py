#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:02 PM
# author: liteng

from bottom.nodes.node import Node


class Neo(Node):

    def __init__(self, config, index, cwd_dir):
        Node.__init__(self, config)
        self.tag = "[bottom.nodes.neo.Neo]"
        self.index = index
        self.cwd_dir = cwd_dir

    def reset_config(self, num: int, update_content: dict):
        Node.reset_config_common(self, self.index, "neo", num)
