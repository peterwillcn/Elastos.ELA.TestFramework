# !/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:29
# file: jar.py

import os
import time
import subprocess

from src.middle.tools import util
from src.middle.tools import constant
from src.middle.tools.log import Logger
from src.bottom.services import net

"""JarService is a class that support jar services

Jar services can create private key, public key, address, transactions and so on
"""


class JarService(object):
    def __init__(self, root_path):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.process = None
        self.running = False
        self.rpc_port = 8989
        self.url = "http://127.0.0.1:8989"
        self.command = "java -cp " + root_path + "/datas/jars/" + constant.JAR_ELA_OLD + constant.JAR_HTTP_SERVICE
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

    def gen_tx(self, inputs, outputs, memo=None):
        if memo is None:
            return net.post_request(
                self.url,
                method="gentx",
                params={"transaction": {"inputs": inputs, "outputs": outputs}}
            )
        else:
            return net.post_request(
                self.url,
                method="gentx",
                params={"transaction": {"inputs": inputs, "outputs": outputs, "memo": memo}}
            )

    def gen_register_producer_tx(self, inputs, outputs, privatekeysign, payload):
        return net.post_request(
            self.url,
            method="genregisterproducertx",
            params={
                "transaction": {
                    "inputs": inputs,
                    "outputs": outputs,
                    "privatekeysign": privatekeysign,
                    "payload": payload
                }
            }
        )

    def gen_update_producer_tx(self, inputs, outputs, privatekeysign, payload):
        return net.post_request(
            self.url,
            method="genupdateproducertx",
            params={
                "transaction": {
                    "inputs": inputs,
                    "outputs": outputs,
                    "privatekeysign": privatekeysign,
                    "payload": payload
                }
            }
        )

    def gen_cancel_producer_tx(self, inputs, outputs, privatekeysign, payload):
        return net.post_request(
            self.url,
            method="gencancelproducertx",
            params={
                "transaction": {
                    "inputs": inputs,
                    "outputs": outputs,
                    "privatekeysign": privatekeysign,
                    "payload": payload
                }
            }
        )

    def gen_return_deposit_coint_tx(self, inputs, outputs, privatekeysign):
        return net.post_request(
            self.url,
            method="genreturndepositcointx",
            params={
                "transaction": {
                    "inputs": inputs,
                    "outputs": outputs,
                    "privatekeysign": privatekeysign
                }
            }
        )

    def gen_activate_producer_tx(self, inputs, outputs, privatekeysign, payload):
        return net.post_request(
            self.url,
            method="genactivateproducertx",
            params={
                "transaction": {
                    "inputs": inputs,
                    "outputs": outputs,
                    "privatekeysign": privatekeysign,
                    "payload": payload
                }
            }
        )

    def gen_vote_tx(self, inputs, outputs, privatekeysign):
        return net.post_request(
            self.url,
            method="genvotetx",
            params={
                "transaction": {
                    "inputs": inputs,
                    "outputs": outputs,
                    "privatekeysign": privatekeysign
                }
            }
        )

    def gen_pledge_address(self, publickey: str):
        return net.post_request(
            self.url,
            method="genpledgeaddress",
            params={"publickey": publickey}
        )

    def gen_cross_chain_transaction(self, inputs, outputs, privatekeysign, crosschainasset):
        return net.post_request(
            self.url,
            method="gencrosschaintx",
            params={
                "transaction": {
                    "inputs": inputs,
                    "outputs": outputs,
                    "privatekeysign": privatekeysign,
                    "crosschainasset": crosschainasset
                }
            }
        )

    def gen_genesis_address(self, block_hash):
        return net.post_request(
            self.url,
            method="gengenesisaddress",
            params={"blockhash": block_hash}
        )



