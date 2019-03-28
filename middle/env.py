#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/3/28 3:11 PM
# author: liteng

import os
import time

from top import config


class Environment(object):

    def __init__(self):
        self.home_path = self.get_env_path("HOME")
        self.go_path = self.get_env_path("GOPATH")
        self.elastos_path = os.path.join(self.go_path, "src/github.com/elastos")
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
            "ela": config.ela,
            "arbiter": config.arbiter,
            "did": config.did,
            "token": config.token,
            "neo": config.neo
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

    e = Environment()
    print(e.home_path)
    print(e.go_path)
    print(e.elastos_path)
    print(e.test_path)