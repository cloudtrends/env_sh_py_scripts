# -*- coding: utf-8 –*-
import sys
reload(sys)
import os
sys.setdefaultencoding('utf8')
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs
import signal
import time

if __name__ == "__main__":
    """
    """
    if 3 != len(sys.argv)
        comm_funcs.print_error(" arguments : app_type and instance_name  need assigned ")
        comm_funcs.print_error(  "ERROR EXIT PYTHON" )
        sys.exit(1)
    gopath = comm_funcs.get_gopath()
    if gopath is None or 0 == len(gopath):
        comm_funcs.print_error("ERROR: evn path not set , prod mod")
        sys.exit(1)
    app_type = sys.argv[1]
    instance_name = sys.argv[2]
    instance_targz_full_path = gopath + "/" + app_type + "/" + instance_name + ".tar.gz"
    if not os.path.exists( instance_targz_full_path ):
        comm_funcs.print_error("ERROR: instance_targz_full_path not set:" + instance_targz_full_path)
        sys.exit(1)
    inst_ports_lines = comm_funcs.get_file_content_as_list(goapth + "/" + "instance_and_ports.txt")
    inst_port = ""
    for one in inst_ports_lines:
        one = one.strip()
        if 0 == one:
            continue
        ones = one.split(",")
        if 2 != len(ones):
            continue
        inst = ones[0].strip()
        if inst != instance_name:
            continue
        port = ones[1].strip()
        inst_port = port
        break
    if 0 == len(inst_port):
        comm_funcs.print_error("ERROR: port of " + instance_name + " not found.")
        sys.exit(1)
    os.system(gopath + "/kill_port_ps.sh " + inst_port)
    unique_file_name = instance_name + "_" + str( time.time() ) + ".bak" 
    os.system("mv " + gopath + "/" + app_type + "/" + instance_name + " " + gopath + "/" + app_type + "/" + unique_file_name )
    os.system("./tar_zxf.sh " + gopath + "/" + app_type +  " " + instance_name + ".tar.gz" + " " + instance_name + " " + app_type)







