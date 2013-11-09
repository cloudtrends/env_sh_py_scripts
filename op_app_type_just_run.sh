#!/bin/bash

APP_PORT=$1
SITE=$2
APP_TYPE=$3

if [ -z ${APP_PORT} ];then
    echo "app port is nil"
    exit 1
fi

if [ -z ${SITE} ];then
    echo "app site is nil"
    exit 1
fi

if [ -z ${APP_TYPE} ];then
    echo "app site is nil"
    APP_TYPE=gobbs
fi

### ### ### ### ### ### ### ### ### 
python prod_config_run.py ${APP_TYPE} ${SITE}


#PID=`lsof -i:${APP_PORT} -t`
#echo "pid is :${PID}"
#kill -9 ${PID}

#cd /home/prebuild-conf/

#./deploy_remote.sh gobbs   gobbs   ${SITE}  

#cd /home/golang/gobbs/${SITE}/

#nohup ./run.sh &

PID=`lsof -i:${APP_PORT} -t`
echo "pid is :${PID}"
echo "END"

