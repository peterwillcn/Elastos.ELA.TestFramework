#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/4 6:25 PM
# author: liteng

import time

from src.control.control import Controller
from src.core.services import rpc
from src.tools.log import Logger

config = {
    "ela": {
        "number": 4,
        "crc_number": 1,
        "pre_connect_offset": 5,
        "crc_dpos_height": 200,
        "public_dpos_height": 208
    },
    "side": False,
    "times": 1
}


def test_content():

    controller = Controller(config)
    will_register_producer = controller.node_manager.ela_nodes[2]
    rpc_port = controller.node_manager.ela_nodes[0].rpc_port
    current_height = controller.get_current_height()
    Logger.debug("current height: {}".format(current_height))

    controller.tx_manager.register_producer(will_register_producer)
    controller.discrete_mining_blocks(1)
    list_producers_nickname = controller.get_list_producers_names()
    producer_status_resp = rpc.producer_status(
        will_register_producer.owner_account.public_key())
    Logger.debug("producers status: {}".format(producer_status_resp))
    producer = controller.tx_manager.register_producers_list[0]
    ret = producer.cancel(rpc_port)
    Logger.debug("cancel producer result: {}".format(ret))
    Logger.info("before cancel list producers: {}".format(list_producers_nickname))
    Logger.info("after cancel list producers:  {}".format(controller.get_list_producers_names()))

    result = len(controller.get_list_producers_names()) != 2
    controller.check_result("cancel pending register list producer has two same nicknames", result)
    controller.terminate_all_process(result)


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)