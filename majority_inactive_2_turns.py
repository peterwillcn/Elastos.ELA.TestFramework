#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.control import Controller
from src.core.services import rpc
from src.tools.log import Logger

config = {
    "ela": {
        "number": 20,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": False,
    "times": 1
}


def test_content():

    # test case title
    test_case = "More than 1/3 producers inactive first rotation still failed but second rotation"
    # init controller for deploy, start nodes and recharges some nodes for registered as producers
    controller = Controller(config)
    # register and vote producers ready for h2 phase
    controller.ready_for_dpos()

    # get some important parameters for later use
    number = controller.params.ela_params.number
    crc_number = controller.params.ela_params.crc_number
    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    # prepare inactive producers [9, 10, 11, 12, 13, 14, 15, 16]
    inactive_producers = controller.tx_manager.register_producers_list[crc_number: crc_number * 3]
    # prepare replace candidate [17, 18, 19, 20]
    replace_cadidates = controller.tx_manager.register_producers_list[crc_number * 3: crc_number * 4]

    # get inactive node public key
    inactive_public_keys = list()
    for producer in inactive_producers:
        inactive_public_keys.append(producer.node.node_keystore.public_key.hex())

    # get replace node public key
    replace_public_keys = list()
    for producer in replace_cadidates:
        replace_public_keys.append(producer.node.node_keystore.public_key.hex())

    global result
    global activate
    global remaining_start
    activate = False
    remaining_start = False
    stop_height = 0

    # mining to the height h1 - pre_connect_offset - 1 (300 - 5 - 1 = 294)
    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    # get number of times of the same height
    height_times = dict()
    height_times[current_height] = 1

    while True:

        # get current height and the number of times it appears
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.info("current height: {}, times: {}".format(current_height, times))

        # if times is more than 1000, that means 1000 times at a certain height, this is unreasonable and \
        # the process will exit
        if times >= 1000:
            result = False
            break

        # after h1, will show current and next current arbiters info
        if current_height >= h1:
            controller.show_current_next_info()

        # when current height is equal h2 + 12(320), then will stop the inactive \
        # producer nodes[9, 10, 11, 12, 13, 14, 15, 16]
        if stop_height == 0 and current_height >= h2 + 12:
            for producer in inactive_producers:
                producer.node.stop()

            # stop height is equal h2 + 12 (320)
            stop_height = current_height
            controller.check_result("Ater H2，stop 1/3 producers and candidates", True)
            Logger.debug("stop_height: {}".format(stop_height))

        # when current is not equal stop height, that means replace candidate promoted to producer and consensus
        if not activate and stop_height != 0 and current_height > stop_height + 36:
            arbiters_set = set(rpc.get_arbiters_info()["arbiters"])
            result = not set(inactive_public_keys).issubset(arbiters_set) and \
                            set(replace_public_keys).issubset(arbiters_set)

            controller.check_result("rotation check", result)

            if result:

                # activate producers [9,10,11,12]
                activate_producers = inactive_producers[:4]

                # first start activate producers nodes
                for producer in activate_producers:
                    producer.node.start()

                controller.discrete_mining_blocks(1)

                # second, ac ativate producers
                for producer in activate_producers:
                    result = controller.tx_manager.activate_producer(producer)
                    controller.check_result("activate producer {}".format(producer.node.name), result)

                activate = True

        if not remaining_start and stop_height != 0 and current_height > stop_height + 80:
            remaining_inactive_producers = inactive_producers[4:]
            for producer in remaining_inactive_producers:
                producer.node.start()
            remaining_start = True

        if stop_height != 0 and current_height > stop_height + 100:
            current_pubkeys = controller.get_current_arbiter_public_keys()
            result = set(controller.rpc_manager.normal_dpos_pubkeys) == set(current_pubkeys) \
                     and controller.check_nodes_height()
            break

        # mining a block per second
        controller.discrete_mining_blocks(1)
        time.sleep(1)

    # Finally, output the test result and exit
    controller.check_result(test_case, result)
    if result:
        controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)



