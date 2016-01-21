#!/bin/bash

LOGS_DIR=$HOME/src/logs
LOGS=(iapi.err iapi.log sapi.err kannel-routing.log sms-routing.err)
PY=python3
TAILER_DIR=$HOME/src/python3-logtailer

# Kill logtailer clients
arr=($(ps aux | grep "$PY .*localclient.py" | awk '{print $2}')); for pid in ${arr[@]}; do kill $pid; done

for log in ${LOGS[@]}; do
	$PY $TAILER_DIR/scripts/localclient.py $LOGS_DIR/$log &
done

