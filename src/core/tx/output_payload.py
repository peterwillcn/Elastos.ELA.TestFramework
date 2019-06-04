#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/1 1:57 PM
# author: liteng


class OutputPayload(object):

    def data(self):
        return None

    def serialize(self):
        return None

    def deserialize(self):
        return None

    def get_version(self):
        return 0

    def validate(self):
        return None

    def __repr__(self):
        return ""