#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/20 10:07 AM
# author: liteng

import time

from src.top.control import Controller
from src.middle.tools.log import Logger


config = {
    "ela": {
        "number": 12,
        "crc_number": 4,
        "pre_connect_offset": 5,
        "crc_dpos_height": 300,
        "public_dpos_height": 308
    },
    "side": True,
    "arbiter": {
        "enable": True,
        "number": 9,
        "pow_chain": True,
        "print_level": 0
    },
    "did": {
        "enable": True,
        "number": 5,
        "instant_block": True
    },
    "times": 1
}


if __name__ == '__main__':

    controller = Controller(config)
    controller.middle.ready_for_dpos()

    h1 = controller.middle.params.ela_params.crc_dpos_height
    h2 = controller.middle.params.ela_params.public_dpos_height
    pre_offset = config["ela"]["pre_connect_offset"]

    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_mining_blocks(h1 - pre_offset - 1 - current_height)

    height_times = dict()
    height_times[current_height] = 1

    while True:
        current_height = controller.get_current_height()
        times = controller.get_height_times(height_times, current_height)
        Logger.debug("current height: {}, times: {}".format(current_height, times))
        if times > 100:
            controller.test_result("cross transaction stop a arbiter or a did", False)
            break

        if current_height > h2 + 12:

            controller.middle.node_manager.arbiter_nodes[1].stop()
            ret = controller.middle.tx_manager.cross_chain_transaction("did", True)
            controller.test_result("stop one arbiter, test cross recharge", ret)

            controller.middle.node_manager.did_nodes[1].stop()
            ret = controller.middle.tx_manager.cross_chain_transaction("did", True)
            controller.test_result("stop one did , test cross recharge", ret)

            # ret = controller.middle.tx_manager.cross_chain_transaction(False)
            # controller.test_result("stop one arbiter, test cross withdraw", ret)

            if ret:
                break
        controller.discrete_mining_blocks(1)
        time.sleep(1)

    controller.terminate_all_process()

