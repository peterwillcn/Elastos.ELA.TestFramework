# !/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:29
# file: jar.py

import os
import time
import subprocess
from middle.common import constant
from bottom.logs.log import Logger
from bottom.services import net

"""JarService is a class that support jar services

Jar services can create private key, public key, address, transactions and so on
"""


class JarService(object):
    def __init__(self):
        self.tag = "[bottom.services.jar.JarService]"
        self.process = None
        self.running = False
        self.rpc_port = 8989
        self.url = "http://127.0.0.1:8989"
        self.command = "java -cp " + "./jars/" + constant.JAR_NAME + constant.JAR_HTTP_SERVICE
        self.start()

    def start(self):
        self.process = subprocess.Popen(self.command, stdout=open(os.devnull, "w"), shell=True)
        self.running = True
        time.sleep(2)
        if self.process is not None:
            Logger.debug("Jar services starts ")

    def stop(self):
        if not self.running:
            return

        try:
            self.process.terminate()
        except subprocess.SubprocessError as e:
            Logger.error("unable to stop jar services. %s" % e)
        Logger.debug("Java services is stopped")
        self.running = False

    def create_transaction(self, inputs, outputs, memo=None):
        if memo is None:
            return net.post_request(self.url, "gentx", params={"transaction": {"inputs": inputs, "outputs": outputs}})
        else:
            return net.post_request(self.url, "gentx",
                                    params={"transaction": {"inputs": inputs, "outputs": outputs, "memo": memo}})

    def register_producer_transaction(self, inputs, outputs, privatekeysign, payload):
        return net.post_request(self.url, "genregisterproducertx",
                                params={
                                    "transaction": {
                                        "inputs": inputs,
                                        "outputs": outputs,
                                        "privatekeysign": privatekeysign,
                                        "payload": payload}
                                })

    def update_producer_transaction(self, inputs, outputs, privatekeysign, payload):
        return net.post_request(self.url, "genupdateproducertx",
                                params={
                                    "transaction": {
                                        "inputs": inputs,
                                        "outputs": outputs,
                                        "privatekeysign": privatekeysign,
                                        "payload": payload}
                                })

    def cancel_producer_transaction(self, inputs, outputs, privatekeysign, payload):
        return net.post_request(self.url, "gencancelproducertx",
                                params={
                                    "transaction": {
                                        "inputs": inputs,
                                        "outputs": outputs,
                                        "privatekeysign": privatekeysign,
                                        "payload": payload}
                                })

    def redemption_producer_transaction(self, inputs, outputs, privatekeysign):
        return net.post_request(self.url, "genreturndepositcointx",
                                params={
                                    "transaction": {
                                        "inputs": inputs,
                                        "outputs": outputs,
                                        "privatekeysign": privatekeysign}
                                })

    def vote_transaction(self, inputs, outputs, privatekeysign):
        return net.post_request(self.url, "genvotetx",
                                params={
                                    "transaction": {
                                        "inputs": inputs,
                                        "outputs": outputs,
                                        "privatekeysign": privatekeysign}
                                })

    def gen_deposit_address(self, publickey: str):
        return net.post_request(self.url, "genpledgeaddress", params={"publickey": publickey})

