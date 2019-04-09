#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 5:13 PM
# author: liteng

import time

from src.top.control import Controller

from src.middle.tools.log import Logger


if __name__ == '__main__':

    controller = Controller()
    controller.middle.ready_for_dpos()
    index = controller.middle.params.ela_params.crc_number + 1
    stop_height = 0
    while True:
        current_height = controller.get_current_height()
        Logger.info("[main] current height: {}".format(current_height))
        if current_height == controller.middle.params.ela_params.public_dpos_height \
            + controller.middle.params.ela_params.crc_number * 3:
            controller.middle.node_manager.ela_nodes[index].stop()
            stop_height = current_height
            Logger.error("[main] node {} stopped at height {} on success!".format(index, stop_height))

        if current_height == stop_height + 2000:
            break
        time.sleep(1)
        controller.discrete_mining_blocks(1)

    controller.terminate_all_process()