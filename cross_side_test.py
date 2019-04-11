#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 11:32 AM
# author: liteng

import time

from src.middle.tools.log import Logger

from src.top.control import Controller

config = {
    "ela": {
        "number": 12,
        "crc_number": 4,
        "crc_dpos_height": 100000,
        "public_dpos_height": 200000
    },
    "side": True,
    "arbiter": {
        "enable": True,
        "number": 9,
        "pow_chain": True,
        "print_level": 0
    },
    "did": {
        "enable": True,
        "number": 5,
        "instant_block": True
    }
}


def cross_chain_before_h1():
    controller = Controller(config)
    time.sleep(3)
    controller.middle.tx_manager.cross_chain_transaction(True)
    time.sleep(2)
    controller.middle.tx_manager.cross_chain_transaction(False)
    time.sleep(1)
    controller.terminate_all_process()


def cross_chain_between_h1_and_h2():
    controller = Controller(config)
    controller.middle.ready_for_dpos()
    time.sleep(3)
    current_height = controller.get_current_height()
    while current_height <= controller.middle.params.ela_params.public_dpos_height + 10:
        controller.discrete_mining_blocks(1)
        time.sleep(0.5)
        current_height = controller.get_current_height()
        Logger.debug("{} current height: {}".format("[main]", current_height))
    controller.middle.tx_manager.cross_chain_transaction(True)
    time.sleep(2)
    controller.middle.tx_manager.cross_chain_transaction(False)
    time.sleep(1)
    controller.terminate_all_process()


if __name__ == '__main__':

    cross_chain_before_h1()