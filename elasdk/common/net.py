#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/23 2:38 PM
# author: liteng

import requests


def get_request(url):
    try:
        response = requests.get(url)
        resp = response.json()
        if resp["Desc"] == "Success":
            return resp["Result"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        return False


def post_request(url, method, params):
    try:
        response = requests.post(url, json={"method": method, "params": params},
                             headers={"content-type": "application/json"})
        resp = response.json()
        if resp["error"] == None:
            return resp["result"]
        else:
            return resp["error"]
    except requests.exceptions.RequestException as e:
        return False


