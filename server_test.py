#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/18 5:48 PM
# author: liteng

import os
from tests.dpos_test import DposTest

from src.tools.log import Logger


if __name__ == '__main__':

    case1 = "dpos_normal_test"
    case2 = "rotation_onebyone_test"
    case3 = "rotation_whole_test"
    case4 = "inactive_single_test"
    case5 = "majority_inactive_1_turn"
    case6 = "majority_inactive_2_turns"
    case7 = "majority_inactive_crc_degradation"
    case8 = "insufficient_producer_degradation_pre_connect"
    case9 = "insufficient_producer_degradation_first_inactive"
    case10 = "insufficient_producer_degradation_cancel_no_stop"
    case11 = "insufficient_producer_degradation_cancel_and_stop"
    case12 = "inactive_crc_test"
    case13 = "cross_normal_test"

    for i in range(1, 14):
        Logger.info("Begin testing case{}".format(i))
        os.system("python3 case{}.py > ./datas/server_test_result/case{}.log".format(i, i))
        Logger.info("Finish testing case{}".format(i))


