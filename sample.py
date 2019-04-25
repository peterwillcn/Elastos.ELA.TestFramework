#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/4/17 2:43 PM
# author: liteng


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

    format_test()



