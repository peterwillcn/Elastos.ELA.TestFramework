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
from core.deal.transaction import Transaction
from core.wallet.keystoremanager import KeyStoreManager


class Controller(object):

    def __init__(self):
        self.tag = '[core.control.Controller]'
        self.jar_service = JarService()
        self.wallets_list = KeyStoreManager(constant.KEYSTORE_INIT_NUMBER).key_stores
        self.rpc_service = RPC()
        self.rest_service = REST()
        self.deploy = Deploy(jar_service=self.jar_service, rpc=self.rpc_service, rest=self.rest_service,
                             key_stores=self.wallets_list)
        self.tx = Transaction(jar_service=self.jar_service, rpc=self.rpc_service, rest=self.rest_service)

        self.deploy.deploy_nodes()
        self.deploy.start_nodes()
        Logger.info('{} Initialize the control successfully')

    def shutdown(self):
        self.jar_service.stop()
        self.deploy.stop_nodes()
