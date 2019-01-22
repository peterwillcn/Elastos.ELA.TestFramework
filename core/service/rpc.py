#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:35 PM
# author: liteng

import requests
from configs import constant
from logs.log import Logger


class RPC(object):

    def __init__(self):
        self.host = 'http://' + constant.LOCAL_HOST
        self.tag = '[RPC Service]'

    def post_request(self, method, port: int, params):
        try:
            url = self.host + ':' + str(port)
            Logger.debug('{} post request url: {}'.format(self.tag, url))
            resp = requests.post(url, json={"method": method, "params": params},
                                 headers={"content-type": "application/json"})
            response = resp.json()
            if response[constant.POST_RESPONSE_ERROR] == None:
                return response[constant.POST_RESPONSE_RESULT]
            else:
                return response[constant.POST_RESPONSE_ERROR]
        except requests.exceptions.RequestException as e:
            return False

    def get_connection_count(self, port: int):
        return self.post_request(constant.METHOD_CONNECTION_COUNT, port, params={})

    def discrete_mining(self, port: int, n: int):
        return self.post_request(constant.METHOD_DISCRETE_MINING, port, params={"count": str(n)})

    def get_wallet_balance(self, port: int, address: str):
        return self.post_request(constant.METHOD_WALLET_BALANCE, port, params={"address": address})

    def send_raw_transaction(self, port: int, data):
        return self.post_request(constant.METHOD_SEND_RAW_TRANSACTION, port, params={"data": data})


