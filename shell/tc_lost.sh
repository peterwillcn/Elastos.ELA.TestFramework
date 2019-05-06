#!/bin/bash

count=5
success=30
time=60

sudo tc qdisc add dev eth0 root netem loss ${count}% ${success}%
echo "before sleep ${time} seconds"
sleep ${time}
echo "after  sleep ${time} s, terminate the tc process"
sudo tc qdisc del dev eth0 root