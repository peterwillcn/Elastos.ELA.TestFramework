#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/4 11:13 PM
# author: liteng

import time

from src.top.control import Controller
from src.middle.tools.log import Logger
from src.middle.tools import constant

from src.bottom.tx.producer import Producer


config = {
    "ela": {
        "number": 4,
        "crc_number": 1,
        "pre_connect_offset": 5,
        "crc_dpos_height": 3000,
        "public_dpos_height": 3008
    },
    "side": False,
    "times": 1
}


def test_content():

    controller = Controller(config)
    crc_number = controller.middle.params.ela_params.crc_number

    current_height = controller.get_current_height()
    Logger.debug("current height: {}".format(current_height))

    # normal transaction test
    tap_keystore = controller.get_tap_keystore()
    output_addresses = list()

    for keystore in controller.middle.keystore_manager.owner_key_stores:
        output_addresses.append(keystore.address)

    Logger.debug("before tap address value: {}".format(
        controller.middle.service_manager.rpc.get_balance_by_address(tap_keystore.address)
    ))

    for address in output_addresses:
        Logger.debug("before target address values: {}".format(
            controller.middle.service_manager.rpc.get_balance_by_address(address)
        ))

    result = controller.middle.tx_manager.tx.transfer_asset(
        input_keystore=tap_keystore,
        output_addresses=output_addresses,
        amount=10000 * constant.TO_SELA
    )

    controller.discrete_mining_blocks(1)
    Logger.debug("after tap address value : {}".format(
        controller.middle.service_manager.rpc.get_balance_by_address(tap_keystore.address)
    ))

    for address in output_addresses:
        Logger.debug("after target address values:  {}".format(
            controller.middle.service_manager.rpc.get_balance_by_address(address)
        ))
    controller.test_result("transfer asset", result)

    # register producer transaction test
    will_register_node = controller.middle.node_manager.ela_nodes[crc_number + 1]

    producer = Producer(will_register_node)
    ret = producer.register(True)
    controller.test_result("register producer", ret)

    # register producer transaction test
    will_register_node2 = controller.middle.node_manager.ela_nodes[crc_number + 2]

    producer = Producer(will_register_node2)
    ret = producer.register(True)
    controller.test_result("register producer2", ret)

    # vote producer transaction test
    candidate_list = list()
    candidate_list.append(will_register_node.owner_keystore.public_key)
    candidate_list.append(will_register_node2.owner_keystore.public_key)

    ret = controller.middle.tx_manager.tx.vote_producer(
        keystore=will_register_node.owner_keystore,
        amount=10 * constant.TO_SELA,
        candidates_list=candidate_list
    )
    controller.test_result("vote producer", ret)

    # update producer transaction test
    before_update_nicknames = controller.get_list_producers_nicknames()
    before_update_nicknames.sort()

    producer.info.nickname = "NickName ^_^"
    producer.info.gen_signature()
    ret = producer.update()

    after_update_nicknames = controller.get_list_producers_nicknames()
    after_update_nicknames.sort()
    controller.discrete_mining_blocks(1)

    Logger.info("before update: {}".format(before_update_nicknames))
    Logger.info("after update : {}".format(after_update_nicknames))
    controller.test_result("update producer: ", ret)

    # cancel producer transaction test
    before_state = controller.get_producer_state(1)
    ret = producer.cancel()
    after_state = controller.get_producer_state(1)
    Logger.info("before cancel state: {}".format(before_state))
    Logger.info("after  cancel state: {}".format(after_state))

    controller.test_result("cancel producer: ", ret)

    # redeem producer transaction test
    controller.discrete_mining_blocks(2170)
    current_height = controller.get_current_height()
    Logger.debug("current height: {}".format(current_height))
    before_balance = controller.middle.service_manager.rpc.get_balance_by_address(producer.deposit_address)
    ret = producer.redeem()
    after_balance = controller.middle.service_manager.rpc.get_balance_by_address(producer.deposit_address)
    Logger.debug("before redeem deposit balance: {}".format(before_balance))
    Logger.debug("after  redeem deposit balance: {}".format(after_balance))

    controller.test_result("redeem producer", ret)
    controller.terminate_all_process()


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)

