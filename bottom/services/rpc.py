#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:35 PM
# author: liteng

from middle.common import constant, util
from bottom.services import net


class RPC(object):

    def __init__(self):
        self.tag = "[bottom.services.rpc.RPC]"
        self.host = "http://127.0.0.1"
        self.port = 10014

    def post_request(self, method, params):
        url = self.host + ":" + str(self.port)
        return net.post_request(url, method, params)

    def get_info(self):
        return self.post_request("getinfo", params={})

    def get_connection_count(self):
        return self.post_request("getconnectioncount", params={})

    def discrete_mining(self, n: int):
        return self.post_request("discretemining", params={"count": str(n)})

    def get_balance_by_address(self, address: str):
        return self.post_request("getreceivedbyaddress", params={"address": address})

    def send_raw_transaction(self, data):
        return self.post_request("sendrawtransaction", params={"data": data})

    def list_unspent_utxos(self, addresses, assetid=None):
        if assetid is None:
            return self.post_request("listunspent", params={"addresses": [addresses]})
        else:
            return self.post_request("listunspent", params={"addresses": [addresses], "assetid": assetid})

    def toggle_mining(self, mining: bool):
        return self.post_request("togglemining", params={"mining": mining})

    def get_block_count(self):
        return self.post_request("getblockcount", params={})

    def get_best_block_hash(self):
        return self.post_request("getbestblockhash", params={})

    def get_block_by_hash(self, blockhash: str, verbosity=2):
        return self.post_request("getblock", params={"blockhash": blockhash, "verbosity": verbosity})

    def get_block_by_height(self, height: int):
        return self.post_request("getblockbyheight", params={"height": height})

    def get_block_hash_by_height(self, height: int):
        return self.post_request("getblockhash", params={"height": height})

    def get_raw_mempool(self):
        return self.post_request("getrawmempool", params={})

    def get_raw_transaction(self, txid, verbose=True):
        return self.post_request("getrawtransaction", params={"txid": txid, "verbose": verbose})

    def get_neighbors(self):
        return self.post_request("getneighbors", params={})

    def get_node_state(self):
        return self.post_request("getnodestate", params={})

    def get_arbitrator_group_by_height(self, height: int):
        return self.post_request("getarbitratorgroupbyheight", params={"height": height})

    def set_log_level(self, level: int):
        return self.post_request("setloglevel", params={"level": level})

    def list_producers(self, start: int, limit: int):
        return self.post_request("listproducers", params={"start": start, "limit": limit})

    def vote_status(self, address: str):
        return self.post_request("votestatus", params={"address": address})

    def producer_status(self, publickey: str):
        return self.post_request("producerstatus", params={"publickey": publickey})