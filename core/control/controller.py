#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/25 3:49 PM
# author: liteng

from logs.log import Logger
from configs import constant
from core.deploy.deploy import Deploy
from core.service.jar import JarService
from core.service.rpc import RPC
from core.service.rest import REST
from core.wallet.keystore import KeyStore
from core.deal.assist import Assist
from core.deal.transaction import Transaction
from core.deal.transaction import Payload
from core.deal.transaction import Producer
from core.deal.transaction import Voter
from core.wallet.keystoremanager import KeyStoreManager


class Controller(object):

    def __init__(self, num=constant.KEYSTORE_INIT_NUMBER):
        self.tag = '[core.control.Controller]'
        self.jar_service = JarService()
        self.wallets_list = KeyStoreManager(num).key_stores
        self.rpc_service = RPC()
        self.rest_service = REST()
        self.assist = Assist(self.rpc_service, self.rest_service)
        self.deploy = Deploy(jar_service=self.jar_service, rpc=self.rpc_service, rest=self.rest_service,
                             key_stores=self.wallets_list)
        self.tx = Transaction(jar_service=self.jar_service, assist=self.assist)
        self.deploy.deploy_nodes()
        self.deploy.start_nodes()
        Logger.info('{} Initialize the control successfully')

    def create_a_producer(self, owner_addr: KeyStore, node_addr: KeyStore, nickname: str):
        load = Payload(
            privatekey=owner_addr.private_key.hex(),
            owner_publickey=owner_addr.public_key.hex(),
            node_publickey=node_addr.public_key.hex(),
            nickname=nickname,
            url="www.test.com",
            location=0,
            address="127.0.0.1"
        )

        pro = Producer(
            keystore=owner_addr,
            payload=load,
            jar_service=self.jar_service,
            assist=self.assist
        )
        Logger.info('{} Create a Producer, nickname: {}'.format(self.tag, nickname))
        return pro

    def create_a_voter(self, keystore: KeyStore, candidates: list):
        vote = Voter(
            keystore=keystore,
            candidates=candidates,
            jar_service=self.jar_service,
            assist=self.assist
        )
        return vote

    def discrete_mining_blocks(self, num: int):
        self.rpc_service.discrete_mining(num)

    def get_balance_by_address(self, address: str):
        return self.rpc_service.get_balance_by_address(address)

    def shutdown(self):
        self.jar_service.stop()
        self.deploy.stop_nodes()


