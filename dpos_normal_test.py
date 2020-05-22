#!/usr/bin/env python

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
        "public_dpos_height": 308,
        "cr_committee_start_height": 350
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    h3 = controller.params.ela_params.cr_committee_start_height
    pre_offset = config["ela"]["pre_connect_offset"]

    current_height = controller.get_current_height()

    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

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
            break

        if current_height >= h1:
            controller.show_arbiter_info()

        if current_height == h1 + 1:
            Logger.info("H1 PASS!")
            Logger.info("H1 PASS!")

        if current_height == h2 + 2:
            Logger.info("H2 PASS!")
            Logger.info("H2 PASS!")

            # register cr
            controller.ready_for_cr()

        # crc proposal
        if current_height == h3 + 1:
            controller.ready_for_crc_proposal()
            controller.ready_for_crc_proposal_review()
            controller.ready_for_crc_proposal_tracking()
            controller.ready_for_crc_proposal_withdraw()
            break
        controller.discrete_mining_blocks(1)
        time.sleep(0.5)

    controller.terminate_all_process()


if __name__ == '__main__':
    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)
