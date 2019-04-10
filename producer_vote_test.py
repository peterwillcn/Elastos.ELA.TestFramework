#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 3:21 PM
# author: liteng

from src.top.control import Controller
from src.middle.tools.log import Logger


if __name__ == '__main__':
    controller = Controller()
    controller.forbidden_side_chain()
    controller.middle.params.ela_params.number = 5
    controller.middle.params.ela_params.crc_number = 1
    controller.middle.params.ela_params.crc_dpos_height = 100000
    controller.middle.params.ela_params.public_dpos_height = 200000

    controller.middle.tx_manager.recharge_producer_keystore()
    ret = controller.middle.tx_manager.register_producers_candidates()
    if ret:
        Logger.info("[main] register producers on success!")
    ret = controller.middle.tx_manager.update_produces_candidates()
    if ret:
        Logger.info("[main] update producers on success!")
    ret = controller.middle.tx_manager.cancel_producers_candidates()
    if ret:
        Logger.info("[main] cancel producers on success!")
    ret = controller.middle.tx_manager.redeem_producers_candidates()
    if ret:
        Logger.info("[main] redeem producers on success!")

    controller.terminate_all_process()


