#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:01 PM
# author: liteng

from src.middle.tools import util

from src.bottom.nodes.node import Node
from src.bottom.parameters.did_params import DidParams


class DidNode(Node):

    def __init__(self, index, config, params: DidParams , cwd_dir):
        Node.__init__(self, config)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.index = index
        self.params = params
        self.cwd_dir = cwd_dir

    def reset_config(self, num: int, update_content: dict):
        Node.reset_config_common(self, self.index, "did", num)