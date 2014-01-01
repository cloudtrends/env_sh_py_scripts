# -*- coding: utf-8 –*-
import sys
reload(sys)
import os
sys.setdefaultencoding('utf8')
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs


def print_error(text):
    comm_funcs.print_error(text)
def print_ok(text):
    comm_funcs.print_ok(text)

def listdir_fullpath(d):
    return comm_funcs.listdir_fullpath(d)



def clean_tmp_dir( tmp_dir ):
    for (dirpath, dirnames, filenames) in os.walk(tmp_dir):
        for filename in filenames:
            #print "tmp dir files:", dirpath + "/" + filename
            os.remove( dirpath + "/" + filename )


def clean_go_file( tmp_dir ):
    for (dirpath, dirnames, filenames) in os.walk(tmp_dir):
        for filename in filenames:
            #print "tmp dir files:", dirpath + "/" + filename
            if filename.endswith( ".go" ):
                os.remove( dirpath + "/" + filename )


def post_prepare_tmp_dir(app_type, TmpAppTypeDir, AppTypeTarFile ):
    if not os.path.isfile( AppTypeTarFile ):
        print_error( AppTypeTarFile + " can not find . " )
        print_error("Exit")
        sys.exit(1)
    shutil.move( AppTypeTarFile , TmpAppTypeDir )
    child = subprocess.Popen(["./tar_zxf.sh",  TmpAppTypeDir ,  AppTypeTarFile , app_type ], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = child.communicate()
    print out
    print err
    os.remove( TmpAppTypeDir + "/" + AppTypeTarFile )
    clean_go_file( TmpAppTypeDir )

def prepare_tmp_dir( app_type , TmpAppTypeDir, AppTypeTarFile ):
    CurrPath = os.getcwd()
    CurrTmpDir = CurrPath + "/tmp"
    #TmpAppTypeDir = CurrTmpDir + "/" + app_type
    if not os.path.exists( CurrTmpDir ):
        os.makedirs( CurrTmpDir )
    else:
        os.system("rm -rf " + CurrTmpDir + "/" + app_type )
        clean_tmp_dir( CurrTmpDir )
    if not os.path.exists( TmpAppTypeDir ):
        os.makedirs( TmpAppTypeDir )
    if os.path.isfile( AppTypeTarFile ):
        os.remove( AppTypeTarFile )
        print_ok( "Remove old tar file :" + AppTypeTarFile )


def package_app(app_type):
    child = subprocess.Popen(["revel", "package", app_type], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = child.communicate()
    if '' == err:
        pass
    else:
        print_error( " when package " + app_type  )
        print_error( "out:"+out )
        print_error( "err:"+err )

def config_conf_and_routes(app_type, TmpAppTypeDir, InstancePreBuildConfDir):
    """
    delete old app.conf
    generate new : routes file
    """
    AppConfDir = TmpAppTypeDir + "/src/" + app_type + "/conf" 
    if not os.path.exists( AppConfDir ):
        print_error("Error AppConfDir not exit :" + AppConfDir)
        sys.exit(1)
    if os.path.exists( AppConfDir + "/app.conf"  ):
        os.remove( AppConfDir + "/app.conf"  )
        os.system( "rm -f " +  AppConfDir + "/app.conf"   )
    if os.path.exists( AppConfDir + "/routes" ):
        os.remove( AppConfDir + "/routes"  )
        os.system( "rm -f " +  AppConfDir + "/routes" )
    shutil.copy2(InstancePreBuildConfDir + "/conf/app.conf"  , AppConfDir)
    os.system( "cp "  + InstancePreBuildConfDir + "/conf/app.conf" + "  " + AppConfDir)
    print_ok( "cp "  + InstancePreBuildConfDir + "/conf/app.conf" + "  " + AppConfDir )
    shutil.copy2(InstancePreBuildConfDir + "/conf/routes" , AppConfDir)
    print_ok( "cp " + InstancePreBuildConfDir + "/conf/routes"  + "  " + AppConfDir )
    os.system( "cp " + InstancePreBuildConfDir + "/conf/routes"  + "  " + AppConfDir )
    #generate 
    




def re_tar_app(tmp_dir , tar_file_name , dest_dir):
    """

dir=$1
tar_file=$2
dest_dir=$3

    """
    os.system( "./tar_czf.sh " + tmp_dir + " "  + tar_file_name + " " + dest_dir)
    pass


    
if __name__ == "__main__":
    """
    package list:
        exe file
        src files
            conf
            views
            ....


    destination dir:
        /home/golang/

    """
    pull_cmd = "python test_auto_gitpush.py pull "
    os.system(  pull_cmd  )

    print_ok( """echo "export PKG_CONFIG_PATH=/usr/local/Cellar/sqlite/3.7.17/lib/pkgconfig:${PKG_CONFIG_PATH}"
export PKG_CONFIG_PATH="/usr/local/Cellar/sqlite/3.7.17/lib/pkgconfig:${PKG_CONFIG_PATH}"
" """ )
    if 4 !=  len(sys.argv):
        print_error(" arguments : app_type and instance_name REMOTE SITE all need assigned ")
        print_error(  "ERROR EXIT PYTHON" )
        sys.exit()
    app_type = sys.argv[1]
    instance_name = sys.argv[2]
    remote_site = sys.argv[3]
    app_type = app_type.strip()
    instance_name = instance_name.strip()
    if comm_funcs.check_app_type_and_instance_name(app_type, instance_name):
        comm_funcs.print_ok("check app_type and instance_name OK")
    else:
        print_error(" app_type or instance_name not match")
        sys.exit(1)
    AppTypeTarFile = app_type + ".tar.gz"
    CurrPath = os.getcwd()
    InstanceAppTypeViewsDir = CurrPath + "/src/" + app_type + "_views/" + instance_name
    if not os.path.exists( InstanceAppTypeViewsDir ):
        print_error("ERROR: InstanceAppTypeViewsDir not exist:"+ InstanceAppTypeViewsDir)
        sys.exit(1)
    PreBuildConfDir = CurrPath + "/prebuild-conf"
    TmpAppTypePreBuildConfDir = PreBuildConfDir + "/" + app_type
    InstancePreBuildConfDir = TmpAppTypePreBuildConfDir  + "/" + instance_name
    comm_funcs.print_ok( "InstancePreBuildConfDir: " + InstancePreBuildConfDir )
    CurrTmpDir = CurrPath + "/tmp"
    
    TmpAppTypeDir = CurrTmpDir +"/"+ app_type
    TmpInstanceDir = CurrTmpDir +"/"+ instance_name
    TmpInstanceAppTypeViewsDir = TmpAppTypeDir + "/src/" + app_type + "/app/views"   
    prepare_tmp_dir(app_type, TmpAppTypeDir, AppTypeTarFile)
    print "begin deploy ... "
    package_app(app_type)
    post_prepare_tmp_dir(app_type, TmpAppTypeDir, AppTypeTarFile )
    config_conf_and_routes(app_type, TmpAppTypeDir , InstancePreBuildConfDir)
    if os.path.exists( TmpInstanceAppTypeViewsDir + "/" + instance_name ):
        print_error("CAUTION === === === === === === === === CAUTION")
        print_error("Why not clean old views of instance_name ")
        os.system( "rm -rf " + TmpInstanceAppTypeViewsDir + "/" + instance_name  )
    os.system( "cp -rf " + InstanceAppTypeViewsDir + " " + TmpInstanceAppTypeViewsDir + "/")
    #shutil.copytree( InstanceAppTypeViewsDir ,  TmpInstanceAppTypeViewsDir + "/" )  
    InstanceTarFile = instance_name + ".tar.gz"
    dest_dir = "./" + instance_name
    #change name from app_type to instance name
    os.system( "mv " + TmpAppTypeDir + " " + TmpInstanceDir  )
    re_tar_app( CurrTmpDir , InstanceTarFile , dest_dir )
    #
    #upload to ....
    # ssh remotehost "rm -f /home/golang/app_type/instance_name.tar.gz"
    if remote_site == "localhost" :
        cmd_str = " rm -rf /home/golang/" + app_type + "/" + instance_name 
        os.system( cmd_str )
        cmd_str = " mkdir -p  /home/golang/" + app_type + "/"
        os.system( cmd_str )
        cmd_str = " cp  " + CurrTmpDir + "/" + InstanceTarFile + " /home/golang/" + app_type
        os.system( cmd_str )
        pass
    else:
        os.system( " ssh  " + remote_site + "\" rm -f /home/golang/" + app_type + "/" +  InstanceTarFile )
        os.system( " scp  " + CurrTmpDir + "/" + InstanceTarFile +"  " + remote_site + ":/home/golang/" + app_type + "/" )










