#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:28
# file: node.py


from configs import constant


class Node(object):

    def __init__(self, config):
        self.config = config

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self, index):
       pass


class MainNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self, index):
        self._reset_port(constant.NODE_PORT_INFO, index)
        self._reset_port(constant.NODE_PORT, index)
        self._reset_port(constant.NODE_PORT_REST, index)
        self._reset_port(constant.NODE_PORT_JSON, index)
        self._reset_port(constant.NODE_PORT_WS, index)

    def _reset_port(self, port_type: str, index: int):
        port = self.config[constant.NODE_CONFIG][port_type]
        port = port % constant.NODE_PORT_BASE
        port = port % constant.NODE_PORT_DIFF
        port = constant.NODE_PORT_BASE + index * constant.NODE_PORT_DIFF + port
        self.config[constant.NODE_CONFIG][port_type] = port


class ArbiterNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self, index):
        pass


class DidNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self, index):
        pass


class TokenNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self, index):
        pass


class NeoNode(Node):

    def start(self):
        pass

    def stop(self):
        pass

    def reset_config(self, index):
        pass


