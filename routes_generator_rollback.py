
import sys

import os
import subprocess
import comm_funcs
import signal
import time
import subprocess
import shutil


SelfHeader = "###begin: self_header"
SelfHeaderEnd = "###end: self_header"

CommonPart = "###begin: common_part"
CommonPartEnd = "###end: common_part"

SelfPart = "###begin: self_part"
SelfPartEnd = "###end: self_part"


def check_routes_file_valid( routes_file_name ):
    """

    """
    contents = comm_funcs.get_file_content_as_list( routes_file_name )
    self_header_flag = False
    self_header_end_flag = False

    common_part_flag = False
    common_part_end_flag = False

    self_part_flag = False
    self_part_end_flag = False
    for line in contents:
        if line.startswith( SelfHeader ):
            self_header_flag = True
        if line.startswith( SelfHeaderEnd ):
            self_header_end_flag = True
        if line.startswith( CommonPart ):
            common_part_flag = True
        if line.startswith( CommonPartEnd ):
            common_part_end_flag = True
        if line.startswith( SelfPart ):
            self_part_flag = True
        if line.startswith( SelfPartEnd ):
            self_part_end_flag = True
    if self_header_flag and self_header_end_flag and common_part_flag and common_part_end_flag and self_part_flag and self_part_end_flag:
        return True
    return False



def __extract_route_one_part(  routes_file_name , begin_part , end_part ):
    contents = comm_funcs.get_file_content_as_list( routes_file_name )
    record_begin = False
    return_lines = ""
    return_lines = return_lines + begin_part + "\n"
    for line in contents:
        if line.startswith( begin_part ):
            record_begin = True
            continue
        if line.startswith( end_part ):
            record_begin = False
            break
        line = line.strip()
        if 0 == len(line):
            continue
        if record_begin:
            return_lines = return_lines + line + "\n"
    return_lines = return_lines + end_part + "\n"
    return return_lines


def extract_self_part( routes_file_name ):
    return __extract_route_one_part( routes_file_name , SelfPart , SelfPartEnd )
def extract_common_part( routes_file_name ):
    return __extract_route_one_part( routes_file_name , CommonPart , CommonPartEnd )
def extract_self_headers( routes_file_name):
    return __extract_route_one_part( routes_file_name , SelfHeader , SelfHeaderEnd )


if __name__ == "__main__":
    if 5 != len(sys.argv):
        comm_funcs.print_error("PYTHON ERROR: argv count not match")
        comm_funcs.print_error("ERROR , EXIT PYTHON")
        sys.exit(1)
    app_type = sys.argv[1]
    instance_name = sys.argv[2]
    direction = sys.argv[3]
    is_check_app_type_and_instance_name = sys.argv[4]
    app_type = app_type.strip()
    instance_name = instance_name.strip()
    if "true" == is_check_app_type_and_instance_name:
        """
        """
        if comm_funcs.check_app_type_and_instance_name(app_type, instance_name):
            comm_funcs.print_ok("check app_type and instance_name OK")
        else:
            comm_funcs.print_error("ERROR: app_type or instance_name not match")
            sys.exit(1)

    print direction
    curr_dir = os.getcwd()
    prebuild_conf_debug_conf_routes_file = curr_dir + "/prebuild-conf/" + app_type + "/local_debug/conf/routes"
    if not os.path.isfile( prebuild_conf_debug_conf_routes_file ):
        comm_funcs.print_error("ERROR: can not find : " + prebuild_conf_debug_conf_routes_file)
        sys.exit(1)
    if not check_routes_file_valid( prebuild_conf_debug_conf_routes_file ):
        comm_funcs.print_error( "ERROR: check self header common_part self_part :" + prebuild_conf_debug_conf_routes_file)
        sys.exit(1)
    prebuild_conf_instance_conf_routes_file =  curr_dir + "/prebuild-conf/" + app_type + "/"+ instance_name +"/conf/routes"
    if not os.path.isfile( prebuild_conf_instance_conf_routes_file ):
        comm_funcs.print_error("ERROR: can not find : " + prebuild_conf_instance_conf_routes_file)
        sys.exit(1)
    if not check_routes_file_valid( prebuild_conf_instance_conf_routes_file ):
        comm_funcs.print_error( "ERROR: check self header common_part self_part :" + prebuild_conf_instance_conf_routes_file)
        sys.exit(1)
    debug_conf_routes = curr_dir + "/src/" + app_type + "/conf/routes"
    if "generate" == direction:
        """
        delete debug conf routes file
        """
        
        print "step 1 : delete DEBUG routes : " , debug_conf_routes
        if os.path.exists( debug_conf_routes ):
            os.remove( debug_conf_routes )
        # step two
        print "step2 : touch a new conf file"
        # step theree
        print "step 3 : generate self header ( copy from prebuild-conf ) "
        self_header_lines = extract_self_headers( prebuild_conf_debug_conf_routes_file )
        common_part_lines = extract_common_part( prebuild_conf_debug_conf_routes_file )
        self_part_lines = extract_self_part( prebuild_conf_instance_conf_routes_file )
        all_lines = self_header_lines + "\n" + common_part_lines + "\n" + self_part_lines + "\n"
        print "step 4: write to "
        os.system( "touch " + debug_conf_routes )
        comm_funcs.add_to_exist_file( debug_conf_routes  , all_lines  )
        pass
    if "rollback" == direction:
        self_header_lines = extract_self_headers( prebuild_conf_instance_conf_routes_file )
        common_part_lines = extract_common_part( debug_conf_routes )
        self_part_lines = extract_self_part( debug_conf_routes )
        all_lines = self_header_lines + "\n" + common_part_lines + "\n" + self_part_lines + "\n"
        #
        #
        os.system( "rm -f " + prebuild_conf_instance_conf_routes_file )
        os.system( "touch " + prebuild_conf_instance_conf_routes_file )
        comm_funcs.add_to_exist_file( prebuild_conf_instance_conf_routes_file  , all_lines  )
        #
        comm_funcs.print_ok( "back up each time changing of :" + debug_conf_routes);
        unique_file_name = str( time.time() ) + "_routes.bak" 
        comm_funcs.print_ok( unique_file_name ) 
        cp_cmd =  debug_conf_routes + " " + curr_dir + "/prebuild-conf/" + app_type + "/local_debug/conf/" + unique_file_name 
        os.system( "cp " + cp_cmd )
        #
        # remove old : prebuild_conf_debug_conf_routes_file
        __self_header_lines = extract_self_headers( prebuild_conf_debug_conf_routes_file )
        __common_part_lines = extract_common_part( debug_conf_routes )
        __self_part_lines   = extract_self_part( prebuild_conf_debug_conf_routes_file )
        __all_lines = __self_header_lines + "\n" + __common_part_lines + "\n" + __self_part_lines + "\n"
        if os.path.exists( prebuild_conf_debug_conf_routes_file ):
            os.remove( prebuild_conf_debug_conf_routes_file )
        os.system( "rm -f " + prebuild_conf_debug_conf_routes_file )
        os.system( "touch " + prebuild_conf_debug_conf_routes_file )
        comm_funcs.add_to_exist_file( prebuild_conf_debug_conf_routes_file  , __all_lines  )
        #
        if os.path.exists( debug_conf_routes ):
            os.remove( debug_conf_routes )
        pass

    print "GO INTO PYTHON, now generate routes "
    comm_funcs.print_ok("OK AND DONE, EXIT PYTHON")
    sys.exit(0)

