# -*- coding: utf-8 –*-
import sys
reload(sys)
import os
sys.setdefaultencoding('utf8')
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs




if __name__ == "__main__":
    gopath = comm_funcs.get_gopath()
    if 0 == len(gopath):
        comm_funcs.print_error( "ERROR GOPATH not set." )
        sys.exit(1)
    comm_funcs.print_ok( "gopath is :" + gopath )
    files = comm_funcs.listdir_fullpath( gopath )
    for one in files:
        print one
        if not os.path.isfile( one ):
            continue
        if one.endswith(".sh") or one.endswith(".py"):
            os.remove(one)
    self_files = comm_funcs.listdir_fullpath( os.getcwd() )
    for one in self_files:
        print one
        if not os.path.isfile( one ) or  "sync_myself" in one :
            continue
        if one.endswith(".sh") or one.endswith(".py"):
            comm_funcs.print_ok("sync " + one + " to ../ " )
            os.system( "cp " + one + " "  + " ../" )
