#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
# author: liteng

import time

from src.middle.tools.log import Logger
from src.top.control import Controller

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 12,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.middle.ready_for_dpos()
    h1 = controller.middle.params.ela_params.crc_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        if current_height == controller.middle.params.ela_params.crc_dpos_height + 1:
            Logger.info("H1 PASS!")
            Logger.info("H1 PASS!")

        if current_height == controller.middle.params.ela_params.public_dpos_height + 2:
            Logger.info("H2 PASS!")
            Logger.info("H2 PASS!")

        if current_height == controller.middle.params.ela_params.public_dpos_height + \
                controller.middle.params.ela_params.crc_number * 3 * 20:     # 2 代表H2后跑2轮共识，修改此数字可多修改几轮
            result = True
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.test_result("Dpos Normal Test", result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


