#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 18:00
# file: main.py

from utils import util
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
    balance = controller.get_balance_by_address(test_address)
    Logger.info('after transaction balance: {}'.format(balance))

    controller.shutdown()


def func2():
    tag = 'Main Test'
    Logger.level = 1
    controller = Controller(40)

    foundation_keystore = controller.wallets_list[0]
    keystores = controller.wallets_list[10:]

    print('keystores length: ', len(keystores))
    util.assert_equal(len(keystores), 30)
    addresses = []
    for keystore in keystores:
        addresses.append(keystore.address)

    result = controller.tx.ordinary_single_sign(foundation_keystore, addresses, 20000 * TO_SELA)
    if not result:
        Logger.error('{} ordinary single sign transaction error!'.format(tag))
    Logger.info('{} ordinary single sign transaction success1'.format(tag))

    producers = []

    i = 0
    all_register = True
    while i < 20:
        pro = controller.create_a_producer(keystores[i], keystores[i+1], nickname='arbiter00' + str(i))
        result = pro.register()
        if not result:
            Logger.error('{} producer {} register failed!'.format(tag, pro.payload.nickname))
            all_register = False
            break
        producers.append(pro)
        i = i + 2
    if all_register:
        Logger.info('{} register {} producers success!'.format(tag, len(producers)))

    all_update = True
    i = 0
    for producer in producers:
        producer.payload.nickname = 'nickname-00' + str(i)
        result = producer.update()
        if not result:
            Logger.error('{} producer {} update failed!'.format(tag, producer.payload.nickname))
            all_update = False
            break
        i = i + 1

    if all_update:
        Logger.info('{} update {} producers success!'.format(tag, len(producers)))

    voter = controller.create_a_voter(keystores[1], producers)
    result = voter.vote()
    if not result:
        Logger.error('{} vote failed!'.format(tag))
        return
    Logger.info('{} vote success!'.format(tag))

    all_cancelled = True
    for pro in producers:
        result = pro.cancel()
        if not result:
            Logger.error('{} producer {} cancelled failed!'.format(tag, pro.payload.nickname))
            all_cancelled = False
            break
    if all_cancelled:
        Logger.info('{} all producers cancelled success!'.format(tag))

    controller.discrete_mining_blocks(2160)

    all_redeem = True
    for pro in producers:
        result = pro.redeem()
        if not result:
            Logger.error('{} producer {} redeem failed!'.format(tag, pro.payload.nickname))
            all_redeem = True
            break

    if all_redeem:
        Logger.info('{} all producers redeem success！'.format(tag))

    controller.shutdown()


if __name__ == "__main__":
    func2()


