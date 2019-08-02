#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/8/1 8:11 PM
# author: liteng

import time
from src.tools.log import Logger
from src.control.control import Controller

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 12,
        "crc_number": 4,
        "later_start_number": 0,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)

    input_account = controller.keystore_manager.tap_account
    register_account = controller.keystore_manager.special_accounts[8]

    nickname = "CR-007"
    url = "www.007.com"

    ret = controller.register_a_cr(
        input_private_key=input_account.private_key(),
        register_private_key=register_account.private_key(),
        nickname=nickname,
        url=url
    )
    Logger.info("result: {}".format(ret))

    # controller.ready_for_dpos()
    controller.discrete_mining_blocks(10)
    controller.terminate_all_process(True)


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)

