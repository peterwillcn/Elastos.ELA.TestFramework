#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
# author: liteng

import time
import random

from src.tools.log import Logger
from src.control import Controller

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 16,
        "crc_number": 4,
        "later_start_number": 4,
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

    first_group_nodes = controller.node_manager.ela_nodes[crc_number * 2 + 1: crc_number * 3 + 1]
    second_group_nodes = controller.node_manager.ela_nodes[crc_number + 1: crc_number * 2 + 1]
    third_group_nodes = controller.node_manager.ela_nodes[1: crc_number + 1]
    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    global result
    global last_change_height
    global last_stop_list
    last_stop_list = list()
    last_change_height = h2

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))

        if times >= 100:
            result = False
            break

        if current_height >= h1:
            controller.show_current_next_info()

        if current_height - last_change_height == 12:
            last_change_height = current_height
            Logger.debug("last change height: {}".format(last_change_height))

            if len(last_stop_list) != 0:
                for node in last_stop_list:
                    node.start()

            result = controller.check_nodes_height()
            controller.check_result("check all nodes height middle", result)

            random_number = random.randint(1, 3)
            last_stop_list.clear()

            if random_number == 1:
                for i in range(3):
                    node = first_group_nodes[i]
                    node.stop()
                    last_stop_list.append(node)

            elif random_number == 2:
                for i in range(3):
                    node = second_group_nodes[i]
                    node.stop()
                    last_stop_list.append(node)

            elif random_number == 3:
                for i in range(3):
                    node = third_group_nodes[i]
                    node.stop()
                    last_stop_list.append(node)

        if current_height >= 1000:
            controller.start_later_nodes()
            result = controller.check_nodes_height()
            controller.check_result("check all nodes height", result)
            break

        if last_change_height == h2:
            controller.discrete_mining_blocks(1)
        else:
            controller.discrete_mining_blocks(5)
        time.sleep(1)

    controller.check_result("Minor nodes stop test", result)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)


