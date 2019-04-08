#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:35 PM
# author: liteng

from src.middle.tools import util
from src.bottom.services import net


class RPC(object):

    DEFAULT_PORT = 10014

    def __init__(self):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.host = "http://127.0.0.1"
        self.default_port = 10014

    def post_request(self, method, params, port: int):
        url = self.host + ":" + str(port)
        return net.post_request(url, method, params)

    def get_info(self, port=DEFAULT_PORT):
        return self.post_request("getinfo", params={}, port=port)

    def get_connection_count(self, port=DEFAULT_PORT):
        return self.post_request("getconnectioncount", params={}, port=port)

    def discrete_mining(self, n: int, port=DEFAULT_PORT):
        return self.post_request("discretemining", params={"count": str(n)}, port=port)

    def get_balance_by_address(self, address: str, port=DEFAULT_PORT):
        return self.post_request("getreceivedbyaddress", params={"address": address}, port=port)

    def send_raw_transaction(self, data, port=DEFAULT_PORT):
        return self.post_request("sendrawtransaction", params={"data": data}, port=port)

    def list_unspent_utxos(self, addresses, assetid=None, port=DEFAULT_PORT):
        if assetid is None:
            return self.post_request("listunspent", params={"addresses": [addresses]}, port=port)
        else:
            return self.post_request("listunspent", params={"addresses": [addresses], "assetid": assetid}, port=port)

    def toggle_mining(self, mining: bool, port=DEFAULT_PORT):
        return self.post_request("togglemining", params={"mining": mining}, port=port)

    def get_block_count(self, port=DEFAULT_PORT):
        return self.post_request("getblockcount", params={}, port=port)

    def get_best_block_hash(self, port=DEFAULT_PORT):
        return self.post_request("getbestblockhash", params={}, port=port)

    def get_block_by_hash(self, blockhash: str, verbosity=2, port=DEFAULT_PORT):
        return self.post_request("getblock", params={"blockhash": blockhash, "verbosity": verbosity}, port=port)

    def get_block_by_height(self, height: int, port=DEFAULT_PORT):
        return self.post_request("getblockbyheight", params={"height": height}, port=port)

    def get_block_hash_by_height(self, height: int, port=DEFAULT_PORT):
        return self.post_request("getblockhash", params={"height": height}, port=port)

    def get_raw_mempool(self, port=DEFAULT_PORT):
        return self.post_request("getrawmempool", params={}, port=port)

    def get_raw_transaction(self, txid, verbose=True, port=DEFAULT_PORT):
        return self.post_request("getrawtransaction", params={"txid": txid, "verbose": verbose}, port=port)

    def get_neighbors(self, port=DEFAULT_PORT):
        return self.post_request("getneighbors", params={}, port=port)

    def get_node_state(self, port=DEFAULT_PORT):
        return self.post_request("getnodestate", params={}, port=port)

    def get_arbitrator_group_by_height(self, height: int, port=DEFAULT_PORT):
        return self.post_request("getarbitratorgroupbyheight", params={"height": height}, port=port)

    def set_log_level(self, level: int, port=DEFAULT_PORT):
        return self.post_request("setloglevel", params={"level": level}, port=port)

    def list_producers(self, start: int, limit: int, port=DEFAULT_PORT):
        return self.post_request("listproducers", params={"start": start, "limit": limit}, port=port)

    def vote_status(self, address: str, port=DEFAULT_PORT):
        return self.post_request("votestatus", params={"address": address}, port=port)

    def producer_status(self, publickey: str, port=DEFAULT_PORT):
        return self.post_request("producerstatus", params={"publickey": publickey}, port=port)