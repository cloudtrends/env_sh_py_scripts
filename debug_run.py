
import sys

import os
import subprocess
import comm_funcs
import signal
import time
import subprocess

def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)


def run_program():
    while True:
        time.sleep(1)
        print("a")
        

if __name__ == "__main__":
    """
    """
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    #
    #
    #
    comm_funcs.helloworld()
    if 2 >= len(sys.argv):
        print "error, should assign: app_type instance_name "
        sys.exit(1)
    app_type = sys.argv[1]
    instance_name = sys.argv[2]
    app_type = app_type.strip()
    instance_name = instance_name.strip()
    if comm_funcs.check_app_type_and_instance_name(app_type, instance_name):
        comm_funcs.print_ok("check app_type and instance_name OK")
    else:
        comm_funcs.print_error("ERROR: app_type or instance_name not match")
        sys.exit(1)
    #run_program()
    try:
        print "export PATH=\"$PATH:$GOPATH/bin\""
        os.system("export PATH=\"$PATH:$GOPATH/bin\"")
        os.system("./debug_run.sh " + app_type + " "  + instance_name )
    except KeyboardInterrupt:
        comm_funcs.print_error( "Ctrl+C capture ")
        sys.exit(1)

