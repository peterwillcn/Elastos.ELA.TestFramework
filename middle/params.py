#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:01 PM
# author: liteng


class Parameter(object):

    def __init__(self, config):
        self.ela_node_enable = config["ela_node_enable"]
        self.arbiter_node_enable = config["arbiter_node_enable"]
        self.did_node_enable = config["did_node_enable"]
        self.token_node_enable = config["token_node_enable"]
        self.neo_node_enable = config["neo_node_enable"]

        self.ela_node_num = config["ela_node_num"]
        self.arbiter_node_num = config["arbiter_node_num"]
        self.did_node_num = config["did_node_num"]
        self.token_node_num = config["token_node_num"]
        self.neo_node_num = config["neo_node_num"]

    def info(self):
        print("ela_enable: ", self.ela_node_enable)
        print("arbiter_enable: ", self.arbiter_node_enable)
        print("did_enable: ", self.did_node_enable)
        print("token_enable: ", self.token_node_enable)
        print("neo_enable: ", self.neo_node_enable)

        print("ela num: ", self.ela_node_num)
        print("arbiter num: ", self.arbiter_node_num)
        print("did num: ", self.did_node_num)
        print("token num: ", self.token_node_num)
        print("neo num: ", self.neo_node_num)
