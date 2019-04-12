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
        "number": 13,
        "crc_number": 4,
        "pre_connect_offset": 20,
        "crc_dpos_height": 210,
        "public_dpos_height": 240      # public_dpos_height - crc_dpos_height should not be equal pre_connect_offset, or panic
    },
    "side": False,
    "stop": True,
    "times": 3
}


def test_content():
    stop = config["stop"]
    control = Controller(config)
    control.middle.ready_for_dpos()
    while True:
        current_height = control.get_current_height()
        Logger.debug("[main] current height: {}".format(current_height))
        control.discrete_mining_blocks(1)
        time.sleep(1)
        if current_height == control.middle.params.ela_params.crc_dpos_height + 1:
            Logger.info("[main] H1 PASS!")
            Logger.info("[main] H1 PASS!")

        if current_height == control.middle.params.ela_params.public_dpos_height + 2:
            Logger.info("[main] H2 PASS!")
            Logger.info("[main] H2 PASS!")

        if current_height == control.middle.params.ela_params.public_dpos_height + \
                control.middle.params.ela_params.crc_number * 3 * 5:
            if stop:
                break

    control.terminate_all_process()


if __name__ == '__main__':

    times = config["times"]
    if times > 1:
        config["stop"] = True

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


