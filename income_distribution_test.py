#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
# author: liteng

import time

from src.tools import constant
from src.tools.log import Logger
from src.control.control import Controller
from src.control.tx_income import TxIncome

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 20,
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

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global vote_height
    global after_h2_transactions
    global last_income_height
    global dpos_votes
    dpos_votes = dict()
    last_income_height = h2
    vote_height = 0
    after_h2_transactions = list()

    register_producers = controller.tx_manager.register_producers_list
    later_vote_producer = register_producers[len(register_producers) - 1]

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        if current_height >= h1:
            controller.show_current_next_info()

        if current_height == h2:
            dpos_votes = controller.get_dpos_votes()

        if current_height > h2 and controller.has_dpos_reward(current_height):
            tx_fee = controller.get_total_tx_fee(after_h2_transactions)
            real_income = controller.get_dpos_real_income(current_height)
            theory_income = controller.get_dpos_theory_income(current_height - last_income_height, tx_fee, dpos_votes)
            result = controller.check_dpos_income(real_income, theory_income)
            controller.check_result("check dpos income", result)
            after_h2_transactions.clear()
            last_income_height = current_height
            dpos_votes = controller.get_dpos_votes()

        if vote_height == 0 and current_height > vote_height + h2 + 20:
            votes = 100
            result = controller.tx_manager.vote_producer(
                keystore=controller.keystore_manager.tap_key_store,
                amount=votes * constant.TO_SELA,
                candidates=[later_vote_producer]
            )

            controller.check_result("vote producer {}".format(later_vote_producer.node.name), result)
            vote_height = current_height

            ti = TxIncome(10000, True)
            after_h2_transactions.append(ti)

        if vote_height != 0 and current_height > vote_height + 500000:
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


