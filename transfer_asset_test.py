#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/4 11:13 PM
# author: liteng

import time

from src.top.control import Controller
from src.middle.tools.log import Logger
from src.middle.tools import constant


config = {
    "ela": {
        "number": 4,
        "crc_number": 1,
        "pre_connect_offset": 5,
        "crc_dpos_height": 200,
        "public_dpos_height": 208
    },
    "side": False,
    "times": 1
}


def test_content():

    controller = Controller(config)

    current_height = controller.get_current_height()
    Logger.debug("current height: {}".format(current_height))

    tap_keystore = controller.get_tap_keystore()
    output_addresses = list()

    for keystore in controller.middle.keystore_manager.node_key_stores:
        output_addresses.append(keystore.address)

    Logger.debug("before tap address value: {}".format(
        controller.middle.service_manager.rpc.get_balance_by_address(tap_keystore.address)
    ))

    for address in output_addresses:
        Logger.debug("before target address values: {}".format(
            controller.middle.service_manager.rpc.get_balance_by_address(address)
        ))

    result = controller.middle.tx_manager.tx.transfer_asset(
        input_keystore=tap_keystore,
        output_addresses=output_addresses,
        amount=100 * constant.TO_SELA
    )

    controller.discrete_mining_blocks(1)
    Logger.debug("after tap address value : {}".format(
        controller.middle.service_manager.rpc.get_balance_by_address(tap_keystore.address)
    ))

    for address in output_addresses:
        Logger.debug("after target address values:  {}".format(
            controller.middle.service_manager.rpc.get_balance_by_address(address)
        ))
    controller.test_result("transfer asset", result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)