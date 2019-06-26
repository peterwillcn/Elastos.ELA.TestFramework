#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:11 PM
# author: liteng

import os
import time

from src.tools import util
from src.core.parameters.params import Parameter


class EnvManager(object):

    def __init__(self):
        self.tag = util.tag_from_path(__file__, self.__class__.__name__)
        self.home_path = self.get_env_path("HOME")
        self.go_path = self.get_env_path("GOPATH")
        print("go path: ", self.go_path)
        self.elastos_path = os.path.join(self.go_path, "src/github.com/elastos")
        print("elastos path: ", self.elastos_path)
        self.test_path = os.path.join(self.home_path, "TestingWork")
        self.current_date_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())

        self.src_path_dict = {
            "ela": "Elastos.ELA",
            "arbiter": "Elastos.ELA.Arbiter",
            "did": "Elastos.ELA.SideChain.ID",
            "token": "Elastos.ELA.SideChain.Token",
            "neo": "Elastos.ELA.SideChain.NeoVM"
        }

        self.config_dict = {
            "ela": Parameter.default_ela_config(),
            "arbiter": Parameter.default_arbiter_config(),
            "did": Parameter.default_did_config(),
            "token": Parameter.default_token_config(),
            "neo": Parameter.default_neo_config()
        }

    @staticmethod
    def get_env_path(env_name):
        path = os.environ.get(env_name)
        if ":" in path:
            env_path = path.split(":")[0]
        else:
            env_path = path

        return env_path


if __name__ == "__main__":

    e = EnvManager()
    print(e.home_path)
    print(e.go_path)
    print(e.elastos_path)
    print(e.test_path)
    print(e.tag)