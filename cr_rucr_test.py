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
        "crc_dpos_height": 300,
        "public_dpos_height": 308,
        "cr_committee_start_height": 100000
    },
    "side": False,
    "times": 1
}


def test_content():
    controller = Controller(config)
    controller.ready_for_dpos()

    h1 = controller.params.ela_params.crc_dpos_height
    h2 = controller.params.ela_params.public_dpos_height

    pre_offset = config["ela"]["pre_connect_offset"]
    current_height = controller.get_current_height()
    if current_height < h1 - pre_offset - 1:
        controller.discrete_miner(h1 - pre_offset - 1 - current_height)

    while True:
        current_height = controller.get_current_height()

        if current_height >= h1:
            controller.show_arbiter_info()

        if current_height == h1 + 1:
            Logger.info("H1 PASS!")
            Logger.info("H1 PASS!")

        if current_height == h2 + 2:
            Logger.info("H2 PASS!")
            Logger.info("H2 PASS!")
            break

        controller.discrete_miner(1)
        time.sleep(0.5)

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

    controller.discrete_miner(7)

    cr_list = controller.get_cr_candidates_list()
    cr_nick_name = cr_list[0]["nickname"]
    cr_state = cr_list[0]["state"]
    Logger.info("cr {} state: {}".format(cr_nick_name, cr_state))

    # update cr
    cr_info.url = "www.elastos.com"
    cr_info.nickname = "HAHA ^_^"
    cr_info.location = 100

    ret = controller.tx_manager.update_cr(
        input_private_key=input_account.private_key(),
        cr_info=cr_info,
    )

    controller.check_result("update a cr: ", ret)

    controller.discrete_miner(2)
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
    controller.discrete_miner(2)
    # cr_list = controller.get_cr_candidates_list()
    # cr_state = cr_list[0]["state"]
    # Logger.info("after unregister a cr, state: {}".format(cr_state))
    # controller.discrete_miner(2160)

    # time.sleep(60)

    # unredeem cr

    balance1 = controller.get_address_balance(cr_info.get_deposit_address())
    ret = controller.tx_manager.redeem_cr(
        crc_info=cr_info,
        return_address=input_account.address(),
        amount=4999 * constant.TO_SELA
    )

    controller.check_result("redeem a cr: ", ret)
    controller.discrete_miner(6)

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
