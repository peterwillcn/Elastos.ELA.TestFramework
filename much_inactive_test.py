#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.top.control import Controller

from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 16,
        "crc_number": 4,
        "pre_connect_offset": 20,
        "crc_dpos_height": 200,
        "public_dpos_height": 230,
        "max_inactivate_rounds": 20
    },
    "side": False,
    "time": 1
}


def much_inactive_test():
    controller = Controller(config)
    controller.middle.ready_for_dpos()
    number =controller.middle.params.ela_params.number
    crc_number = controller.middle.params.ela_params.crc_number
    h2 = controller.middle.params.ela_params.public_dpos_height
    test_case = ">= 1/3 Inactive and Arbiter Rotation"
    inactive_producers_nodes = controller.middle.node_manager.ela_nodes[crc_number: crc_number * 2]

    inactive_public_keys = controller.middle.keystore_manager.node_key_stores[crc_number: crc_number * 2]
    replace_public_keys = controller.middle.keystore_manager.node_key_stores[crc_number * 3: number]
    inactive_set = set(inactive_public_keys)
    replace_set = set(replace_public_keys)
    stop_height = 0

    while True:
        current_height = controller.get_current_height()
        Logger.info("[test] current height: {}".format(current_height))
        controller.discrete_mining_blocks(1)
        if stop_height == 0 and current_height >= h2 + 12:
            controller.test_result("Ater H2", True)

            for node in inactive_producers_nodes:
                node.stop()

            stop_height = current_height
            print("stop_height 1: ", stop_height)
        if stop_height != 0 and current_height > stop_height:
            arbiters_nicknames = controller.get_current_arbiter_nicknames()
            Logger.info("arbiters nicknames: {}".format(arbiters_nicknames))

        if stop_height != 0 and current_height > stop_height + 36:
            arbiters_set = set(controller.middle.service_manager.rpc.get_arbiters_info()["arbiters"])
            ret = not inactive_set.issubset(arbiters_set) and replace_set.issubset(arbiters_set)

            controller.test_result(test_case, ret)
            if ret:
                break
        time.sleep(1)

    controller.terminate_all_process()


if __name__ == '__main__':

    much_inactive_test()




