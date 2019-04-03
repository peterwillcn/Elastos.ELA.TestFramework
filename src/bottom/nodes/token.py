#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:02 PM
# author: liteng

from src.bottom.nodes.node import Node


class Token(Node):

    def __init__(self, config, index, cwd_dir: str):
        Node.__init__(self, config)
        self.tag = "[src.bottom.nodes.token.Token]"
        self.index = index
        self.cwd_dir = cwd_dir

    def reset_config(self, num: int, update_content: dict):
        Node.reset_config_common(self, self.index, "token", num)
