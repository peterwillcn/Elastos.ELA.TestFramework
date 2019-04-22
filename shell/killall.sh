#!/bin/bash 

#killall ela java did arbiter

for i in `seq 50`
do
	ID=`ps -ef | grep "ela$i" | grep -v "grep" | awk '{print $2}'`
	for id in $ID
	do
		kill -9 $id
		echo "killed $id"
	done
done

for i in `seq 10`
do
	ID=`ps -ef | grep "arbiter$i" | grep -v "grep" | awk '{print $2}'`
	for id in $ID
	do
		kill -9 $id
		echo "killed $id"
	done
done


for i in `seq 10`
do
	ID=`ps -ef | grep "did$i" | grep -v "grep" | awk '{print $2}'`
	for id in $ID
	do
		kill -9 $id
		echo "killed $id"
	done
done

killall java

echo "kill all processes!"
