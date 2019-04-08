#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 9:45 AM
# author: liteng

import time

from src.middle.tools.log import Logger
from src.top.control import Controller


if __name__ == '__main__':
    control = Controller()
    while True:
        current_height = control.get_current_height()
        Logger.debug("[main] current height: {}".format(current_height))
        control.discrete_mining_blocks(1)
        time.sleep(2)
        if current_height == control.middle.params.ela_params.public_dpos_height + \
                control.middle.params.ela_params.crc_number * 3 * 3:
            break
    control.terminate_all_process()
