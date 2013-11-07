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
    if 1 == len(sys.argv):
        comm_funcs.print_error(" push or pull ?")
        sys.exit(1)
    push_or_pull = sys.argv[1]
    if push_or_pull not in "push pull":
        comm_funcs.print_error(" what your input is not match push or pull ")
        sys.exit(1)
    gopath = comm_funcs.get_gopath()
    if gopath is None or 0 == len(gopath):
        comm_funcs.print_error("ERROR: evn path not set , prod mod")
        sys.exit(1)
    auto_gitpush_projs = comm_funcs.get_file_content_as_list(gopath + "/" + "auto_gitpush_projs.txt")
    for one in auto_gitpush_projs:
        one = one.strip()
        if 0 == len(one):
            continue
        comm_funcs.print_ok(" relative path :" + one )
        full_path = "./test_auto_gitpush.sh " + gopath + "/" + one + " " + push_or_pull
        comm_funcs.print_ok("full path:"+full_path)
        os.system( full_path )

