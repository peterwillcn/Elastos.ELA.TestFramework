#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/24 11:42 AM
# author: liteng


import time

from src.tools.log import Logger
from sdk.wallet.account import Account
from sdk.tx.producer import Producer
from src.control.control import Controller

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 4,
        "crc_number": 1,
        "later_start_number": 0,
        "pre_connect_offset": 5,
        "crc_dpos_height": 4000,
        "public_dpos_height": 4200
    },
    "side": False,
    "times": 1
}


if __name__ == '__main__':

    c = Controller(config)

    node = c.node_manager.ela_nodes[2]
    rpc_port = 10016
    producer = Producer(
        input_private_key=node.owner_account.private_key(),
        owner_private_key=node.owner_account.private_key(),
        node_private_key=node.node_account.private_key(),
        nick_name="James-007",
        url="http://www.007.com",
        location=0,
        net_address="127.0.0.1:10019"
    )

    tx = producer.register(rpc_port)

    ret = c.tx_manager.handle_tx_result(tx)
    Logger.info("regiser tx: {}".format(tx))
    c.check_result("producer register", ret)

    c.discrete_mining_blocks(6)

    Logger.info("producer owner pubkey: {}".format(producer.owner_public_key()))
    payload = producer.get_payload()
    payload.nickname = "HAHA"
    # payload.node_account = Account()

    tx = producer.update(payload, rpc_port)
    ret = c.tx_manager.handle_tx_result(tx, rpc_port)
    Logger.info("update tx: {}".format(tx))
    Logger.info("producer owner pubkey: {}".format(producer.owner_public_key()))

    c.check_result("producer update", ret)
    time.sleep(1)
    c.discrete_mining_blocks(1)

    tx = producer.cancel(rpc_port)
    ret = c.tx_manager.handle_tx_result(tx, rpc_port)

    Logger.info("producer cancel result: {}".format(ret))
    c.check_result("producer cancel", ret)
    time.sleep(1)
    c.discrete_mining_blocks(2170)

    deposit_address = producer.get_payload().get_deposit_address()
    Logger.debug("before deposit balance: {}".format(c.get_address_balance(deposit_address)))
    tx = producer.redeem(4999 * 100000000, rpc_port)
    c.tx_manager.handle_tx_result(tx, rpc_port)
    c.discrete_mining_blocks(1)

    Logger.debug("after deposit balance: {}".format(c.get_address_balance(deposit_address)))

    c.terminate_all_process()






