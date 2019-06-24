#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
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
    controller.ready_for_dpos()
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]
    crc_number = controller.params.ela_params.crc_number

    current_height = controller.get_current_height()

    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global start_height
    global after_h2_transactions
    global last_income_height
    global dpos_votes
    dpos_votes = dict()
    last_income_height = h2
    after_h2_transactions = list()
    start_height = 0

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        if current_height >= h1:
            controller.show_arbiter_info()

        if current_height == h1 + 1:
            Logger.info("H1 PASS!")
            Logger.info("H1 PASS!")

        if current_height == h2 + 2:
            Logger.info("H2 PASS!")
            Logger.info("H2 PASS!")
            dpos_votes = controller.get_dpos_votes()

        # if current_height > h2 and controller.has_dpos_reward(current_height):
        #     tx_fee = controller.get_total_tx_fee(after_h2_transactions)
        #     real_income = controller.get_dpos_real_income(current_height)
        #     theory_income = controller.get_dpos_theory_income(current_height - last_income_height, tx_fee, dpos_votes)
        #     result = controller.check_dpos_income(real_income, theory_income)
        #     controller.check_result("check dpos income", result)
        #     after_h2_transactions.clear()
        #     last_income_height = current_height
        #     dpos_votes = controller.get_dpos_votes()

        # current is equal 380, start the later nodes include two candidates and two normal nodes
        if start_height == 0 and current_height > h2 + crc_number * 3 * 6:
            controller.start_later_nodes()
            start_height = current_height

        if start_height != 0 and current_height > start_height + 36:
            result = controller.check_nodes_height()
            controller.check_result("check all the nodes height", result)
            break

        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.check_result("Dpos Normal Test", result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


