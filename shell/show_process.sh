#!/bin/bash

ps -e | grep ela\[0-9\] | grep -v grep | grep -v ssh 
ps -e | grep arbiter\[0-9\] | grep -v grep
ps -e | grep did\[0-9\] | grep -v grep
ps -e | grep token\[0-9\] | grep -v grep
ps -e | grep neo\[0-9\] | grep -v grep
ps -e | grep old.jar | grep -v grep
ps -e | grep ela_tool.jar | grep -v grep

