#!/bin/bash

MY_DIR=`dirname $0`
source $MY_DIR/comm_funcs.sh

dir=$1
tar_file=$2
instance_name=$3
app_type=$4

print_ok "cd $dir"
cd $dir

print_ok "begin tar zxf file $tar_file"
tar zxf $tar_file

cd instance_name
nohup ./${app_type} &


