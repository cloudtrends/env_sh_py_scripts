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

import psutil
import socket
import os
import argparse
import json

ACCESS_DENIED = ''

pid_list = psutil.get_pid_list()


maped_pid_list={}
maped_pinfo_list={}

def print_ok( str ):
    print str


def IsPortListening(port_num):
    for pid in pid_list:
        if pid in maped_pid_list:
            p = maped_pid_list[ pid ]
            #print "find p in map"
        else:
            p = psutil.Process(pid)
            maped_pid_list[pid]=p


        if pid in maped_pinfo_list:
            pinfo = maped_pinfo_list[pid]
        else:
            try:
                pinfo = p.as_dict(ad_value=ACCESS_DENIED)
                maped_pinfo_list[pid]=pinfo
            except Exception as ex:
                print ex
                continue
        if pinfo['connections'] != ACCESS_DENIED:
            for conn in pinfo['connections']:
                if conn.type == socket.SOCK_STREAM:
                    #print conn
                    lip, lport = conn.laddr
                    if lport ==  port_num:
                        return True , p
    return False , None

def ForceRestartOneApp( app_obj ):
    params = app_obj["params"]
    params = params.replace( "  ", " " )
    params = params.replace( "  ", " " )
    params = params.replace( "  ", " " )
    params = params.replace( "  ", " " )
    paramss = params.split(" ")
    app_type = paramss[2]
    app_domain = paramss[1]
    cmd_str = " python ./prod_config_run.py " + app_type +  "  " + app_domain
    print_ok( cmd_str )
    #os.system( cmd_str )

def CheckOneApp( app_obj ):
    port= int(app_obj["port"])
    is_run , process_obj = IsPortListening( port )
    if is_run:
        print process_obj
        print str(port)+" ok"
    else:
        action_app = app_obj["action_app"] 
        if action_app.startswith("/"):
            pass
        else:
            action_app = "./" + action_app
        cmd_str = action_app + " " + app_obj["params"]
        os.system( cmd_str ) 
        print str(port) +" is not running"


if __name__ == "__main__":
    #, version='%(prog)s 1.0'
    parser = argparse.ArgumentParser(description='Get a program and run it with input')
    #parser.add_argument('program', type=str, help='Program name')
    #parser.add_argument('infiles', nargs='+', type=str, help='Input text files')
    parser.add_argument('--file', type=str, default='./json_port_monitor.json', help='name of config file')
    args = parser.parse_args()
    if not os.path.exists(  args.file ):
        print " config file not exist :" + args.file
        exit()
    json_content= open( args.file ).read()
    #print json_content
    
    json_obj = json.loads( json_content )
    #print json_obj
    monitor_list = json_obj["monitor_list"]
    for one in monitor_list:
        ForceRestartOneApp( one )
        #CheckOneApp(one)
        #print one

    #print args
    print "ok"
    sys.exit(0)

