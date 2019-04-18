#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/8 3:21 PM
# author: liteng

import time
from src.top.control import Controller
from src.middle.tools.log import Logger

config = {
    "ela": {
        "number": 12,
        "crc_number": 4,
        "crc_dpos_height": 150,
        "public_dpos_height": 170
    },
    "side": False,
    "times": 1
}


def test_content():
    test_case = "Testing Register, Update, Cancel, Redeem a Producer"
    controller = Controller(config)
    controller.forbidden_side_chain()
    crc_number = controller.middle.params.ela_params.crc_number
    total_number = controller.middle.params.ela_params.number
    h1 = controller.middle.params.ela_params.crc_dpos_height
    h2 = controller.middle.params.ela_params.public_dpos_height

    Logger.debug("Step 1, recharge ela nodes who will be registered as a producer")
    controller.middle.tx_manager.recharge_producer_keystore()

    Logger.debug("step 2, {} before H1".format(test_case))
    pre_registered_nodes = controller.middle.node_manager.ela_nodes[crc_number+1: total_number+1]
    index = 0
    ret = controller.middle.tx_manager.tx.register_a_producer(pre_registered_nodes[index])
    controller.test_result("Register a producer before H1", ret)
    controller.show_current_height()

    producer = controller.middle.tx_manager.tx.register_producers_list[index]
    payload = producer.payload
    payload.nickname = "Band-007"
    ret = controller.middle.tx_manager.tx.update_a_producer(producer, payload)
    controller.test_result("Update a producer before H1", ret)
    controller.show_current_height()

    ret = controller.middle.tx_manager.tx.cancel_a_producer(producer)
    controller.test_result("Cancel a producer before H1", ret)
    controller.discrete_mining_blocks(2170)
    controller.show_current_height()

    ret = controller.middle.tx_manager.tx.redeem_a_producer(producer)
    controller.test_result("Redeem a producer before H1", ret)
    controller.show_current_height()
    print("\n")

    Logger.debug("step 3, {} between H1 and H2".format(test_case))

    index += 1
    current_height = controller.get_current_height()
    if current_height < h1:
        controller.discrete_mining_blocks(h1 - current_height + 5)

    ret = controller.middle.tx_manager.tx.register_a_producer(pre_registered_nodes[index], True)
    if ret:
        for i in range(6):
            controller.discrete_mining_blocks(1)
            time.sleep(1)

    producer_status_resp = controller.middle.service_manager.rpc.producer_status(
        pre_registered_nodes[index].owner_keystore.public_key.hex())
    Logger.debug("producers status: {}".format(producer_status_resp))

    net = producer_status_resp == "Activate"
    controller.test_result("Register a producer between H1 and H2", net)
    controller.show_current_height()

    producer = controller.middle.tx_manager.tx.register_producers_list[index]
    payload = producer.payload
    payload.nickname = "Band-007"
    ret = controller.middle.tx_manager.tx.update_a_producer(producer, payload)
    controller.test_result("Update a producer between H1 and H2", ret)
    controller.show_current_height()

    ret = controller.middle.tx_manager.tx.cancel_a_producer(producer)
    controller.test_result("Cancel a producer between H1 and H2", ret)

    controller.test_result(test_case, ret)
    controller.terminate_all_process()


if __name__ == '__main__':

    times = config["times"]
    if times > 1:
        config["stop"] = True

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i+1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i+1))
        time.sleep(3)

