#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/17 2:43 PM
# author: liteng

import  struct


def get_height_times(height_times: dict, height):
    if height not in height_times.keys():
        height_times[height] = 0
    else:
        height_times[height] += 1
    return height_times[height]


def format_test():
    for i in range(21):
        s = "{:0>3d}-crc".format(i)
        print(s)


def height_times_test():
    current_height = 1
    height_times = dict()
    height_times[current_height] = 1

    times = 0
    for i in range(10):
        times = get_height_times(height_times, i)
        if i == 1:
            break

    print("times:", times)


if __name__ == "__main__":

    #format_test()
    n = 99
    r1 = struct.pack("I", n)
    r2 = struct.pack(">I", n)
    print("r1: ", r1.hex())
    print("r2: ", r2.hex())
    a = "0d002102517f74990da8de27d0bc7c516c45ecbb9b2aa6a4d4d5ab552b537e638fcfe45f2024a65e1fd2fb3f305be6bb1d2df9583030d2ff6483300a687f27be99d3a2c2c3018103010203019595c9df90075148eb06860365df33584b75bff782a510c6cd4883a419833d5015006400000001e6aeba372a763f7035f5b7d06c235133b062e4204fc546e1e8f750cf271c55840c00000000000000370200000166bd5b004de8c3fb66b2eacbd774ea2dbcba22be630000000103030405020102"
    b = "0d002102517f74990da8de27d0bc7c516c45ecbb9b2aa6a4d4d5ab552b537e638fcfe45f2024a65e1fd2fb3f305be6bb1d2df9583030d2ff6483300a687f27be99d3a2c2c3018103010203019595c9df90075148eb06860365df33584b75bff782a510c6cd4883a419833d5015006400000001e6aeba372a763f7035f5b7d06c235133b062e4204fc546e1e8f750cf271c55840c00000000000000370200000166bd5b004de8c3fb66b2eacbd774ea2dbcba22be630000000103030405020102"
    print(a is b)
