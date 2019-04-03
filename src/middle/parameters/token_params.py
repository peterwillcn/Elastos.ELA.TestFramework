#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/1 10:42 AM
# author: liteng


class TokenParams(object):
    def __init__(self, config: dict):
        self.tag = "[src.middle.parameters.token_params.TokenParams]"
        self.enable = config["enable"]
        self.number = config["number"]