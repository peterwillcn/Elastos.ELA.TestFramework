#!/bin/bash

echo "terminate the tc process"
sudo tc qdisc del dev eth0 root