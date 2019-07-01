#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/23 2:38 PM
# author: liteng

import requests
from src.tools import util
from src.tools.log import Logger

tag = util.tag_from_path(__file__, "")


def get_request(url):
    try:
        Logger.debug("{} get request url: {}".format(tag, url))
        response = requests.get(url)
        resp = response.json()
        if resp["Desc"] == "Success":
            return resp["Result"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        Logger.error("{} get request error: {}".format(tag, e))
        return False


def post_request(url, method, params):
    try:
        Logger.debug("{} url: {}".format(tag, url))
        Logger.debug("{} method: {}".format(tag, method))
        Logger.debug("{} params: {}".format(tag, params))
        response = requests.post(url, json={"method": method, "params": params},
                             headers={"content-type": "application/json"})
        resp = response.json()
        if resp["error"] == None:
            return resp["result"]
        else:
            return resp["error"]
    except requests.exceptions.RequestException as e:
        Logger.error("{} post request error: {}".format(tag, e))
        return False


if __name__ == "__main__":
    print(tag)