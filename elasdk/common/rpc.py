#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/4 2:47 PM
# author: liteng

from elasdk.common import net

DEFAULT_HOST = "http://127.0.0.1"
DEFAULT_PORT = 10016


def post_request(method, params, port: int):
    url = DEFAULT_HOST + ":" + str(port)
    return net.post_request(url, method, params)


def get_info(port=DEFAULT_PORT):
    return post_request("getinfo", params={}, port=port)


def get_connection_count(port=DEFAULT_PORT):
    return post_request("getconnectioncount", params={}, port=port)


def discrete_mining(n: int, port=DEFAULT_PORT):
    return post_request("discretemining", params={"count": str(n)}, port=port)


def get_balance_by_address(address: str, port=DEFAULT_PORT):
    return post_request("getreceivedbyaddress", params={"address": address}, port=port)


def send_raw_transaction(data, port=DEFAULT_PORT):
    return post_request("sendrawtransaction", params={"data": data}, port=port)


def list_unspent_utxos(address: str, assetid=None, port=DEFAULT_PORT):
    if assetid is None:
        return post_request("listunspent", params={"addresses": [address]}, port=port)
    else:
        return post_request("listunspent", params={"addresses": [address], "assetid": assetid}, port=port)


def get_utxos_by_amount(address: str, amount: str, port=DEFAULT_PORT):
    return post_request("getutxosbyamount", params={"address": address, "amount": amount}, port=port)


def toggle_mining(mining: bool, port=DEFAULT_PORT):
    return post_request("togglemining", params={"mining": mining}, port=port)


def get_block_count(port=DEFAULT_PORT):
    return post_request("getblockcount", params={}, port=port)


def get_best_block_hash(port=DEFAULT_PORT):
    return post_request("getbestblockhash", params={}, port=port)


def get_block_by_hash(blockhash: str, verbosity=2, port=DEFAULT_PORT):
    return post_request("getblock", params={"blockhash": blockhash, "verbosity": verbosity}, port=port)


def get_block_by_height(height: int, port=DEFAULT_PORT):
    return post_request("getblockbyheight", params={"height": height}, port=port)


def get_block_hash_by_height(height: int, port=DEFAULT_PORT):
    return post_request("getblockhash", params={"height": height}, port=port)


def get_raw_mempool( port=DEFAULT_PORT):
    return post_request("getrawmempool", params={}, port=port)


def get_raw_transaction( txid, verbose=True, port=DEFAULT_PORT):
    return post_request("getrawtransaction", params={"txid": txid, "verbose": verbose}, port=port)


def get_neighbors( port=DEFAULT_PORT):
    return post_request("getneighbors", params={}, port=port)


def get_node_state( port=DEFAULT_PORT):
    return post_request("getnodestate", params={}, port=port)


def get_arbitrator_group_by_height( height: int, port=DEFAULT_PORT):
    return post_request("getarbitratorgroupbyheight", params={"height": height}, port=port)


def set_log_level( level: int, port=DEFAULT_PORT):
    return post_request("setloglevel", params={"level": level}, port=port)


def list_producers( start: int, limit: int, port=DEFAULT_PORT):
    return post_request("listproducers", params={"start": start, "limit": limit, "state": "all"}, port=port)


def vote_status( address: str, port=DEFAULT_PORT):
    return post_request("votestatus", params={"address": address}, port=port)


def producer_status( publickey: str, port=DEFAULT_PORT):
    return post_request("producerstatus", params={"publickey": publickey}, port=port)


def get_arbiters_info( port=DEFAULT_PORT):
    return post_request("getarbitersinfo", params={}, port=port)