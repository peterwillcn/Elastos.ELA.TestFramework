#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:01 PM
# author: liteng

from src.bottom.nodes.node import Node


class Did(Node):

    def __init__(self, config, index: int, cwd_dir):
        Node.__init__(self, config)
        self.tag = "[src.bottom.nodes.did.Did]"
        self.index = index
        self.cwd_dir = cwd_dir

    def reset_config(self, num: int, update_content: dict):
        Node.reset_config_common(self, self.index, "did", num)