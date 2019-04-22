#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
# author: liteng

import time
import signal

from src.middle.tools.log import Logger
from src.top.control import Controller

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 12,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 200,
        "public_dpos_height": 208
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.middle.ready_for_dpos()
    h1 = controller.middle.params.ela_params.crc_dpos_height

    while True:
        current_height = controller.get_current_height()
        Logger.debug("[main] current height: {}".format(current_height))
        num = h1 - current_height
        if num > 0:
            controller.discrete_mining_blocks(num)
        else:
            controller.discrete_mining_blocks(1)
        time.sleep(1)

        if current_height == controller.middle.params.ela_params.crc_dpos_height + 1:
            Logger.info("[main] H1 PASS!")
            Logger.info("[main] H1 PASS!")

        if current_height == controller.middle.params.ela_params.public_dpos_height + 2:
            Logger.info("[main] H2 PASS!")
            Logger.info("[main] H2 PASS!")

        if current_height == controller.middle.params.ela_params.public_dpos_height + \
                controller.middle.params.ela_params.crc_number * 3 * 1:     # 2 代表H2后跑2轮共识，修改此数字可多修改几轮
            break
    controller.test_result("Dpos Normal Test", True)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


