#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:29
# file: jar.py

import os
import time
import subprocess
from utils import util
from configs import constant
from logs.log import Logger
from core.service import rpc

"""JarService is a class that support jar service

Jar service can create private key, public key, address, transactions and so on
"""


class JarService(object):
    def __init__(self):
        self.process = None
        self.running = False
        self.rpc_port = 8989
        self.command = "java -cp " + "./jars/" + constant.JAR_NAME + constant.JAR_HTTP_SERVICE
        self.start()

    def start(self):
        self.process = subprocess.Popen(self.command, stdout=open(os.devnull, 'w'), shell=True)
        self.running = True
        time.sleep(2)
        if self.process != None:
            Logger.debug("Jar service starts ")

    def stop(self):
        if not self.running:
            return

        try:
            self.process.terminate()
        except subprocess.SubprocessError as e:
            Logger.error("unable to stop jar service. %s" % e)
        Logger.debug("Java service is stopped")
        self.running = False


    def create_transaction(self, utxos, outputs, memo=None):
        if memo == None:
            return util.post_request("gentx", self.rpc_port,
                                     params={"transaction": {"inputs": utxos, "outputs": outputs}})
        else:
            return util.post_request("gentx", self.rpc_port,
                                     params={"transaction": {"inputs": utxos, "outputs": outputs, "memo": memo}})
