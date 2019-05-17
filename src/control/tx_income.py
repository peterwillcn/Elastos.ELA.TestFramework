#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/17 2:32 PM
# author: liteng


class TxIncome(object):

    def __init__(self, tx_fee=0, valid=True):
        self.tx_fee = tx_fee
        self.valid = valid