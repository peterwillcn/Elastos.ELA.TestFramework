#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 6:02 PM
# author: liteng

import os
import subprocess

from src.tools import util
from src.tools.log import Logger

from src.core.nodes.node import Node
from src.core.parameters.neo_params import NeoParams


class NeoNode(Node):

    def __init__(self, index, config, params: NeoParams, cwd_dir):
        Node.__init__(self, config)
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.index = index
        self.params = params
        self.cwd_dir = cwd_dir
        self.rpc_port = self.reset_port(index, "neo", "json_port")
        self.err_output = open(os.path.join(self.cwd_dir, "error.log"), 'w')
        self.process = None
        self.running = None

    def reset_config(self, num: int, update_content: dict):
        Node.reset_config_common(self, self.index, "neo", num)

    def start(self):
        self.process = subprocess.Popen(
            "./did{}".format(self.index),
            stdout=self.dev_null,
            stderr=self.err_output,
            shell=True,
            cwd=self.cwd_dir
        )
        self.running = True
        Logger.debug("{} ./did{} started on success.".format(self.tag, self.index))
        return True

    def stop(self):
        if not self.running:
            Logger.error("{} did{} has already stopped".format(self.tag, self.index))
            return
        try:
            self.process.terminate()
            self.dev_null.close()
            self.err_output.close()
        except subprocess.SubprocessError as e:
            Logger.error("{} Unable to stop ela{}, error: {}".format(self.tag, self.index, e))
        self.running = False
        Logger.debug("{} did{} has stopped on success!".format(self.tag, self.index))