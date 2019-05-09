#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/18 5:48 PM
# author: liteng

import os
import time
import sys
import signal

from src.tools.log import Logger


def exit_handler(signum, frame):
    print("Toggle the Exit Signal, Exit...")
    time.sleep(1)
    sys.exit("Sorry, Good Bye!")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)

    test_cases = dict()
    test_cases["case1"] = "dpos_normal_test"
    test_cases["case2"] = "rotation_onebyone_test"
    test_cases["case3"] = "rotation_whole_test"
    test_cases["case4"] = "inactive_single_test"
    test_cases["case5"] = "majority_inactive_1_turn"
    test_cases["case6"] = "majority_inactive_2_turns"
    test_cases["case7"] = "majority_inactive_crc_degradation"
    test_cases["case8"] = "insufficient_producer_degradation_pre_connect"
    test_cases["case9"] = "insufficient_producer_degradation_first_inactive"
    test_cases["case10"] = "insufficient_producer_degradation_cancel_no_stop"
    test_cases["case11"] = "insufficient_producer_degradation_cancel_and_stop"
    test_cases["case12"] = "inactive_crc_test"
    test_cases["case13"] = "cross_normal_test"

    current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    path = os.path.join("./datas/server_test_result", current_time)
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(1, 14):

        Logger.info("Begin testing case{}".format(i))
        case = test_cases["case{}".format(i)]
        os.system("python3 {}.py > ./datas/server_test_result/{}/{}.log".format(case, current_time, case))
        Logger.info("Finish testing case{}".format(i))
        os.system("sh ./shell/killall.sh")


