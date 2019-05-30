#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 5:04 PM
# author: liteng

import time
import requests
import signal
import sys

from src.tools.log import Logger


span_time = 2
crc_number = 2
prompt = '> '


def exit_handler(signum, frame):
	print("Toggle the Exit Signal, Exit...")
	time.sleep(1)
	sys.exit("Sorry, Good Bye!")


def post_request(url, method, params):
	try:
		response = requests.post(
			url=url,
			json={"method": method, "params": params},
			headers={"content-type": "application/json"}
		)
		resp = response.json()
		if resp["error"] is None:
			return resp["result"]
		else:
			return resp["error"]
	except requests.exceptions.RequestException as e:
		return False


def get_node_height(port: int):
	url = "http://127.0.0.1:" + str(port)
	response = post_request(
		url=url,
		method="getblockcount",
		params={}
	)
	return response


def get_txpool_size(port: int):
	url = "http://127.0.0.1:" + str(port)
	tx_pool = post_request(url, "getrawmempool", params={})
	if type(tx_pool) == list:
		return len(tx_pool)
	else:
		return False


def print_output(name, height, tx_size, node_height: dict):
	global color_prefix
	global color_tail

	color_prefix = ""
	color_tail = ""

	if name not in node_height.keys():
		node_height[name] = height
	else:
		if node_height[name] == height:
			color_prefix = Logger.COLOR_RED
			color_tail = Logger.COLOR_END
		node_height[name] = height
	print(color_prefix + "{}\theight: {}\t txpool size: {}".format(name, height, tx_size) + color_tail)


if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_handler)

	print("How many nodes will you start: ")
	node_num = input(prompt)
	node_height = dict()

	while True:
		for i in range(int(node_num)):
			port = (100 + i) * 100 + 16
			height = get_node_height(port)
			tx_size = get_txpool_size(port)
			if i == 0:
				name = "miner    "
			elif i <= crc_number:
				name = "crc" + str(i) + "    "
			elif i <= crc_number * 3:
				name = "producer" + str(i)
			else:
				name = "candidate" + str(i)

			print_output(name, height, tx_size, node_height)
		time.sleep(span_time)
		print('*' * 60)
