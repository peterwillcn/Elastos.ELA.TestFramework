#!/bin/bash

ps -e | grep ela\[0-9\] | grep -v grep | grep -v ssh 
ps -e | grep arbiter\[0-9\] | grep -v grep
ps -e | grep did\[0-9\] | grep -v grep
ps -e | grep java | grep -v grep
