#!/bin/bash

MY_DIR=`dirname $0`
source $MY_DIR/comm_funcs.sh

dir=$1
tar_file=$2
dest_dir=$3

print_ok "shell: cd $dir"
cd $dir

print_ok "shell: begin tar czf file $tar_file"
echo $tar_file $dest_dir
tar czf $tar_file  $dest_dir
print_ok "shell: after create tar file "
rm -rf $dest_dir
exit $?