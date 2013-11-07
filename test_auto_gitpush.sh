#!/bin/bash


MY_DIR=`dirname $0`
source $MY_DIR/comm_funcs.sh


cd $1

push_or_pull=$2

if [ "push" == "${push_or_pull}" ];then
    print_ok "begin :${push_or_pull}" 
    git add .
    git commit -am "auto push"
    git push
fi
if [ "pull" == "${push_or_pull}" ];then
    print_ok "begin :${push_or_pull}" 
    git pull
fi
