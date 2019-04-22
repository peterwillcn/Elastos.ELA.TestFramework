#!/bin/bash 

# kill ela process
ids=`ps -ef | grep ela\[0-9\] | awk '{print $2}'`

for id in $ids
do
    echo "kill process ela id $id"
    kill -9 $id
done

# kill arbiter process
ids=`ps -ef | grep arbiter\[0-9\] | awk '{print $2}'`

for id in $ids
do
    echo "kill process arbiter id $id"
    kill -9 $id
done

# kill did process
ids=`ps -ef | grep did\[0-9\] | awk '{print $2}'`

for id in $ids
do
    echo "kill process did id $id"
    kill -9 $id
done

echo "kill process java"
killall java

echo "kill all processes!"
