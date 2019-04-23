#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/1/24 5:04 PM
# author: liteng

import time
import requests
import signal
import sys


span_time = 2
crc_number = 4
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


if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_handler)

	print("How many nodes will you start: ")
	node_num = input(prompt)

	while True:
		for i in range(int(node_num)):
			port = (100 + i) * 100 + 14
			height = get_node_height(port)
			tx_size = get_txpool_size(port)
			if i == 0:
				print("miner     {}\theight: {}\t txpool size: {}".format(i, height, tx_size))
			elif i <= crc_number:
				print("crc       {}\theight: {}\t txpool size: {}".format(i, height, tx_size))
			elif i <= crc_number * 3:
				print("producer  {}\theight: {}\t txpool size: {}".format(i, height, tx_size))
			else:
				print("candidate {}\theight: {}\t txpool size: {}".format(i, height, tx_size))

		time.sleep(span_time)
		print('*' * 60)
