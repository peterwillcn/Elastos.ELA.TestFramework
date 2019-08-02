#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/8/1 8:11 PM
# author: liteng

import time
from src.tools.log import Logger
from src.tools import constant
from src.control.control import Controller

config = {
    "ela": {
        "enable": True,
        "password": "123",
        "number": 12,
        "crc_number": 4,
        "later_start_number": 0,
        "pre_connect_offset": 5,
        "crc_dpos_height": 30000,
        "public_dpos_height": 30800
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)

    input_account = controller.keystore_manager.tap_account
    register_account = controller.keystore_manager.special_accounts[8]
    register_private_key = register_account.private_key()

    # register cr
    nickname = "CR-007"
    url = "www.007.com"

    cr_info = controller.create_cr_info(
        register_private_key=register_private_key,
        nickname=nickname,
        url=url,
        location=0
    )

    ret = controller.tx_manager.register_cr(
        input_private_key=input_account.private_key(),
        amount=5000 * constant.TO_SELA,
        cr_info=cr_info
    )

    Logger.info("result: {}".format(ret))

    i = 7
    while i != 0:
        controller.discrete_mining_blocks(1)
        cr_list = controller.get_cr_candidates_list()
        cr_nick_name = cr_list[0]["nickname"]
        cr_state = cr_list[0]["state"]
        Logger.info("cr {} state: {}".format(cr_nick_name, cr_state))
        i -= 1
    # controller.ready_for_dpos()
    controller.discrete_mining_blocks(1)

    # time.sleep(1)
    # update cr
    cr_info.url = "www.elastos.com"
    cr_info.nickname = "HAHA ^_^"
    cr_info.location = 100

    ret = controller.tx_manager.update_cr(
        input_private_key=input_account.private_key(),
        update_cr_info=cr_info,
    )

    controller.check_result("update a cr: ", ret)

    controller.discrete_mining_blocks(2)
    cr_list = controller.get_cr_candidates_list()
    cr_nick_name = cr_list[0]["nickname"]
    cr_url = cr_list[0]["url"]
    cr_location = cr_list[0]["location"]
    cr_state = cr_list[0]["state"]

    Logger.info("after update cr, nickname: {}".format(cr_nick_name))
    Logger.info("after update cr, location: {}".format(cr_location))
    Logger.info("after update cr, url: {}".format(cr_url))
    Logger.info("after update cr, state: {}".format(cr_state))

    # unregister cr
    ret = controller.tx_manager.unregister_cr(
        input_private_key=input_account.private_key(),
        register_private_key=register_private_key
    )
    controller.check_result("unregister a cr: ", ret)
    controller.discrete_mining_blocks(2)
    # cr_list = controller.get_cr_candidates_list()
    # cr_state = cr_list[0]["state"]
    # Logger.info("after unregister a cr, state: {}".format(cr_state))
    controller.discrete_mining_blocks(2120)

    # time.sleep(60)

    # unredeem cr

    balance1 = controller.get_address_balance(cr_info.get_deposit_address())
    ret = controller.tx_manager.redeem_cr(
        crc_info=cr_info,
        return_address=input_account.address(),
        amount=4999 * constant.TO_SELA
    )

    controller.check_result("redeem a cr: ", ret)
    controller.discrete_mining_blocks(6)

    # cr_list = controller.get_cr_candidates_list()
    # cr_state = cr_list[0]["state"]
    # Logger.info("after redeem a cr, state: {}".format(cr_state))

    balance2 = controller.get_address_balance(cr_info.get_deposit_address())

    Logger.info("before redeem deposit balance: {}".format(balance1))
    Logger.info("after  redeem deposit balance: {}".format(balance2))

    controller.terminate_all_process(True)


if __name__ == '__main__':

    for i in range(config["times"]):
        Logger.warn("[main] begin testing {} times".format(i + 1))
        time.sleep(2)
        test_content()
        Logger.warn("[main] end testing {} times".format(i + 1))
        time.sleep(3)

