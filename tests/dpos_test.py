#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/3 6:20 PM
# author: liteng

import sys
import time
import signal
from src.top.control import Controller

controller = Controller()


def exit_handler(signum, frame):
    print("Toggle the exit signal, exit...")
    controller.terminate_all_process()
    time.sleep(1)
    sys.exit("Sorry, Good Bye!")


def dpos_normal_test():
    signal.signal(signal.SIGINT, exit_handler)
    while True:
        controller.discrete_mining_blocks(1)
        time.sleep(2)
        current_height = controller.get_current_height()
        print("current height: ", current_height)
        if current_height == (controller.middle.params.ela_params.public_dpos_height +
                              controller.middle.params.ela_params.crc_number * 3 * 2):
            break
    time.sleep(5)
    controller.terminate_all_process()


def dpos_exception_test():
    c = Controller()
    time.sleep(5)
    c.terminate_all_process()


if __name__ == "__main__":
    dpos_exception_test()