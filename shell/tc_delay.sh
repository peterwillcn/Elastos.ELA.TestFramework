#!/bin/bash

delay=100
around=10
time=60

sudo tc qdisc add dev eth0 root netem delay ${delay}ms ${around}ms
echo "before sleep ${time} seconds"
sleep ${time}
echo "after  sleep ${time} seconds, terminate the tc process"
ssh nrt401 "sudo tc qdisc del dev eth0 root"