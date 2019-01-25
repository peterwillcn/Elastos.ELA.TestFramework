#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 18:00
# file: main.py

from logs.log import Logger
from core.control.controller import Controller

TO_SELA = 100000000


def func0():
    a = ['abc', 123, 'how']
    if a:
        print("123")
    else:
        print('456')


def func1():
    controller = Controller()
    foundation_keystore = controller.wallets_list[0]
    test_address = controller.wallets_list[len(controller.wallets_list)-1].address

    balance = controller.rest_service.get_balance_by_address(test_address)
    Logger.info('before transaction balance: {}'.format(balance))
    result = controller.tx.ordinary_single_sign(foundation_keystore, [test_address], 10000 * TO_SELA, mode='privatekey')
    if not result:
        Logger.error('transaction error')
        exit(0)
    Logger.info('transaction success.')
    balance = controller.rpc_service.get_balance_by_address(test_address)
    Logger.info('after transaction balance: {}'.format(balance))

    controller.shutdown()


if __name__ == "__main__":
    func1()


