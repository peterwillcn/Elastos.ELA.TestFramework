#!/usr/bin/env python
# encoding: utf-8

# author: liteng
# contact: liteng0313@gmail.com
# time: 2019-01-16 17:29
# file: jar.py

import os
import time
import subprocess
from utils import config
from logs.log import Logger


"""JarService is a class that support jar service

Jar service can create private key, public key, address, transactions and so on
"""


class JarService(object):
    def __init__(self):
        self.process = None
        self.running = False
        self.command = "java -cp " + "./jars/" + config.JAR_NAME + config.JAR_HTTP_SERVICE
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