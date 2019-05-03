#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.top.control import Controller

from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 14,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308,
        "max_inactivate_rounds": 100
    },
    "side": False,
    "times": 3
}


def test_content():
    controller = Controller(config)
    controller.middle.ready_for_dpos()

    crc_number = controller.middle.params.ela_params.crc_number
    h1 = controller.middle.params.ela_params.crc_dpos_height
    h2 = controller.middle.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    stop_height = 0
    test_case = "Single inactive and arbiter rotation"
    inactive_producer_index = 0
    inactive_producer = controller.middle.tx_manager.tx.register_producers_list[inactive_producer_index]

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global activate
    activate = False

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.info("[main] current height: {}, times: {}".format(current_height, times))
        if times > 1000:
            result = False
            break

        if current_height > h1:
            current_nicknames = controller.get_current_arbiter_nicknames()
            next_nicknames = controller.get_next_arbiter_nicknames()

            Logger.debug("current arbiter nicknames: {}".format(current_nicknames))
            Logger.debug("next arbiter nicknames   : {}".format(next_nicknames))

        if stop_height == 0 and current_height >= h2 + 1:
            controller.test_result("Ater H2", True)
            inactive_producer.node.stop()
            stop_height = current_height
            Logger.error(
                "[main] node {} stopped at height {} on success!".format(
                    inactive_producer_index + crc_number + 1,
                    stop_height
                )
            )

        if not activate and stop_height != 0 and current_height >= stop_height + 150:

            state = controller.get_producer_state(inactive_producer_index)
            result = state == "Inactivate"
            controller.test_result("Before active producer, the stopped producer state is Inactive", result)
            result = inactive_producer.activate_without_jar()
            Logger.info("activate the producer result: {}".format(result))
            activate = True

        if stop_height != 0 and current_height > stop_height + 200:
            state = controller.get_producer_state(inactive_producer_index)
            result = state == "Activate"
            break

        time.sleep(1)
        controller.discrete_mining_blocks(1)

    controller.test_result(test_case, result)
    controller.terminate_all_process()


if __name__ == '__main__':

    times = config["times"]

    for i in range(times):
        Logger.info("Start Testing {} times".format(i+1))
        time.sleep(1)
        test_content()
        time.sleep(1)
        Logger.info("End Testing {} times".format(i+1))
