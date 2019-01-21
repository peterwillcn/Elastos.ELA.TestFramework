#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:28
# file: node.py

import os
import subprocess
from logs.log import Logger
from configs import constant


class Node(object):

    def __init__(self, config):
        self.config = config
        self.dev_null = open(os.devnull, 'w')

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self):
        pass


class MainNode(Node):

    def __init__(self, index, data_dir, config):
        Node.__init__(self, config)
        self.tag = '[MainNode]'
        self.index = index
        self.binary = constant.NODE_BINARY_MAIN
        self.data_dir = data_dir
        self.rpc_port = 0
        self.rest_port = 0
        self.process = None
        self.running = False

    def start(self):
        self.process = subprocess.Popen('./' + self.binary + ' -p 123', stdout=self.dev_null,
                                        shell=True, cwd=self.data_dir)
        self.running = True
        Logger.debug('{} {} {} started, waiting for rpc to come up'.format(
                        self.tag, self.binary, self.index))

    def stop(self):
        if not self.running:
            Logger.error('{} {} {} has already stopped'.format(
                            self.tag, self.binary, self.index))
            return
        try:
            self.process.terminate()
        except subprocess.SubprocessError as e:
            Logger.error('{} Unable to stop {} {}, error: {}'.format(
                self.tag, self.binary, self.index, e))
        self.running = False
        Logger.debug('{} {} {} has stopped successfully!'.format(self.tag, self.binary, self.index))

    def reset_config(self):
        self._reset_port(constant.NODE_PORT_INFO, self.index)
        self._reset_port(constant.NODE_PORT, self.index)
        self._reset_port(constant.NODE_PORT_REST, self.index)
        self._reset_port(constant.NODE_PORT_JSON, self.index)
        self._reset_port(constant.NODE_PORT_WS, self.index)
        self._reset_port(constant.NODE_PORT_OPEN, self.index)

    def _reset_port(self, port_type: str, index: int):
        port = self.config[constant.NODE_CONFIG][port_type]
        port = port % constant.NODE_PORT_BASE
        port = port % constant.NODE_PORT_DIFF
        port = constant.NODE_PORT_BASE + index * constant.NODE_PORT_DIFF + port
        self.config[constant.NODE_CONFIG][port_type] = port
        if port_type == constant.NODE_PORT_REST:
            self.rest_port = port
        elif port_type == constant.NODE_PORT_JSON:
            self.rpc_port = port


class ArbiterNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self):
        pass


class DidNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self):
        pass


class TokenNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self):
        pass


class NeoNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self):
        pass


