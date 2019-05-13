#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.control import Controller

from src.tools.log import Logger

config = {
    "ela": {
        "number": 16,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308,
        "max_inactivate_rounds": 50
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()

    crc_number = controller.params.ela_params.crc_number
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    stop_height = 0
    test_case = "Single inactive and arbiter rotation"
    inactive_producer_index = 0

    # producer[PRO-005]
    inactive_producer = controller.tx_manager.register_producers_list[inactive_producer_index]

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global activate
    global check
    global later_start

    result = False
    activate = False
    check = False
    later_start = False

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.info("[main] current height: {}, times: {}".format(current_height, times))
        if times > 1000:
            result = False
            break

        if current_height > h1:
            controller.show_current_next_info()

        if stop_height == 0 and current_height >= h2 + 12:
            controller.check_result("Ater H2", True)
            inactive_producer.node.stop()
            stop_height = current_height
            Logger.error(
                "[main] node {} stopped at height {} on success!".format(
                    inactive_producer_index + crc_number + 1,
                    stop_height
                )
            )

        if not activate and stop_height != 0 and current_height >= stop_height + 60:

            state = controller.get_producer_state(inactive_producer_index)
            result = state == "Inactivate"
            Logger.debug("get producer state: {}".format(state))
            controller.check_result("Before active producer, the stopped producer state is Inactive", result)

            inactive_producer.node.start()
            result = controller.tx_manager.activate_producer(inactive_producer)
            Logger.info("activate the producer result: {}".format(result))
            controller.check_result("send activate producer transaction", result)

            ret = controller.tx_manager.activate_producer(inactive_producer)
            controller.check_result("1 same height and send activate producer again", not ret)

            while True:
                current_height2 = controller.get_current_height()
                if current_height2 - current_height < 6:
                    ret = controller.tx_manager.activate_producer(inactive_producer)
                    controller.check_result("2 pending state and send activate producer again", not ret)
                else:
                    break
                controller.discrete_mining_blocks(1)
                time.sleep(1)

            activate = True

        if not later_start and stop_height != 0 and current_height > stop_height + 80:
            state = controller.get_producer_state(inactive_producer_index)
            result = state == "Activate"
            Logger.debug("activted producer state: {}".format(state))
            controller.check_result("activated producer state is activate", result)
            ret = controller.tx_manager.activate_producer(inactive_producer)
            controller.check_result("3 state is activated send activate producer again", not ret)
            controller.start_later_nodes()
            later_start = True

        if stop_height != 0 and current_height > stop_height + 100:
            result = controller.check_nodes_height()
            controller.check_result("check all the nodes height", result)
            break

        time.sleep(1)
        controller.discrete_mining_blocks(1)

    controller.check_result(test_case, result)
    controller.terminate_all_process()


if __name__ == '__main__':

    times = config["times"]

    for i in range(times):
        Logger.info("Start Testing {} times".format(i+1))
        time.sleep(1)
        test_content()
        time.sleep(1)
        Logger.info("End Testing {} times".format(i+1))
