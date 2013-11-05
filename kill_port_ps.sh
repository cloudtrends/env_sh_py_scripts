#!/bin/bash

APP_PORT=$1

if [ -z ${APP_PORT} ];then
    echo "app port is nil"
    exit 1
fi


PID=`lsof -i:${APP_PORT} -t`
echo "pid is :${PID}"
kill -9 ${PID}


