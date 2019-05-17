#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date: 2019/5/13 3:05 PM
# author: liteng

import random
from decimal import Decimal

if __name__ == '__main__':

       a = 230089979.0
       b = a / 100000000
       print("a = ", a)
       print("b = ", b)

       c = round(b, 7)
       print("c = ", c)
