#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/18 7:35 PM
# author: liteng

from middle import util, constant
from bottom.services import net
from bottom.logs.log import Logger


class REST(object):

    def __init__(self):
        self.tag = "[bottom.services.rest.REST]"
        self.host = "http://" + constant.HOST_NAME
        self.port = util.reset_config_ports(0, constant.NODE_TYPE_MAIN, constant.CONFIG_PORT_REST)

    def get_request(self, url_path):
        url = self.host + ":" + str(self.port) + url_path
        Logger.debug("{} get post url path: {}".format(self.tag, url))
        return net.get_request(url)

    def get_connection_count(self):
        return self.get_request("/api/v1/nodes/connectioncount")

    def get_node_state(self):
        return self.get_request("/api/v1/nodes/state")

    def get_block_height(self):
        return self.get_request("/api/v1/block/height")

    def get_transaction_pool(self):
        return self.get_request("/api/v1/transactionpool")

    def restart(self):
        return self.get_request("/api/v1/restart")

    def get_block_hash_by_height(self, height: int):
        return self.get_request("/api/v1/block/hash/" + str(height))

    def get_block_info_by_height(self, height: int):
        return self.get_request("/api/v1/block/details/height/" + str(height))

    def get_block_info_by_hash(self, hash: str):
        return self.get_request("/api/v1/block/details/hash/" + hash)

    def get_transaction_hashes_by_height(self, height: int):
        return self.get_request("/api/v1/block/transactions/height/" + str(height))

    def get_info_by_transaction_hash(self, tx_hash: str):
        return self.get_request("/api/v1/transaction/" + tx_hash)

    def get_balance_by_address(self, address: str):
        return self.get_request("/api/v1/asset/balances/" + address)

    def get_info_by_asset_hash(self, asset_hash: str):
        return self.get_request("/api/v1/asset/" + asset_hash)

    def get_utxos_by_address(self, address: str):
        return self.get_request("/api/v1/asset/utxos/" + address)

    def get_balance_by_address_asset_id(self, address: str, asset_id: str):
        return self.get_request("/api/v1/asset/balance/" + address + "/" + asset_id)

    def get_utxos_by_address_asset_id(self, address: str, asset_id: str):
        return self.get_request("/api/v1/asset/utxo/" + address + "/" + asset_id)
