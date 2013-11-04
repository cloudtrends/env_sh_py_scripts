#!/bin/bash

MY_DIR=`dirname $0`
source $MY_DIR/comm_funcs.sh

dir=$1
tar_file=$2
app_type=$3

print_ok "cd $dir"
cd $dir

print_ok "begin tar zxf file $tar_file"
tar zxf $tar_file

if [ -f $app_type ];then
    chmod +x $app_type    
else
    print_error "$app_type main app file not found."
fi

if [ -f "run.sh" ];then
    chmod +x run.sh
else
    print_error "run.sh main app file not found."
fi


