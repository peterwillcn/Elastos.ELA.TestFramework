#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 3:21 PM
# author: liteng

import time
from src.top.control import Controller
from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 5,
        "crc_number": 1,
        "crc_dpos_height": 100000,
        "public_dpos_height": 200000
    },
    "side": False,
    "times": 3
}


def test_content():
    controller = Controller(config)
    controller.forbidden_side_chain()

    controller.middle.tx_manager.recharge_producer_keystore()

    ret = controller.middle.tx_manager.register_producers_candidates()
    if ret:
        Logger.info("[main] register producers on success!")
    ret = controller.middle.tx_manager.update_produces_candidates()
    if ret:
        Logger.info("[main] update producers on success!")
    ret = controller.middle.tx_manager.cancel_producers_candidates()
    if ret:
        Logger.info("[main] cancel producers on success!")
    ret = controller.middle.tx_manager.redeem_producers_candidates()
    if ret:
        Logger.info("[main] redeem producers on success!")

    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)

