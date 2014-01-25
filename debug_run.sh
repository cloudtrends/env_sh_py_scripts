#!/bin/bash



ROUTES_GENERATE_ROLLBACK_PY="routes_generator_rollback.py"

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

function rollback_views() {
  print_ok "syncing ... ${APP} "
  mv  ${APP_INSTANCE_VIEWS_DIR} ${REPO_INSTANCE_VIEWS_DIR} 
}

function rollback_routes() {

  print_ok "begin rollback conf to prebuild-conf  : app.conf and routes"
  is_check_app_type_and_instance_name="false"
  python  ${ROUTES_GENERATE_ROLLBACK_PY}  ${APP_TYPE}   ${APP_INSTANCE}  "rollback"   ${is_check_app_type_and_instance_name}
}

sync_views()
# example cleanup function
{
  rollback_views
  rollback_routes


  return $?
}
 

control_c()
# run if user hits control-c
{
  echo -en "\n*** Ouch! Exiting ***\n"
  print_ok "Before stop app , sync for views of :${APP}"
  sync_views


  print_ok "EXIT SHELL , traped the control_c."
  exit $?
}

trap control_c SIGINT
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


MY_DIR=`dirname $0`
source $MY_DIR/comm_funcs.sh

APP_TYPE=$1
APP_INSTANCE=$2

if [ -z ${APP_TYPE} ];then
        print_error "app type name shoud assigned"
        exit 1
fi
if [ -z ${APP_INSTANCE} ];then
        print_error "app instance name shoud assigned"
        exit 1
fi
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


REPO_VIEWS_DIR=${MY_DIR}/src/${APP_TYPE}_views/
REPO_INSTANCE_VIEWS_DIR=${MY_DIR}/src/${APP_TYPE}_views/${APP_INSTANCE}

APP_VIEWS_DIR=${MY_DIR}/src/${APP_TYPE}/app/views
APP_INSTANCE_VIEWS_DIR=${MY_DIR}/src/${APP_TYPE}/app/views/${APP_INSTANCE}


PREBUILD_CONF_DIR=${MY_DIR}/prebuild-conf
APP_INSTANCE_CONF_DIR=${MY_DIR}/src/${APP_TYPE}/conf
LOCAL_DEBUG_CONF_DIR=${PREBUILD_CONF_DIR}/${APP_TYPE}/local_debug

if [ -d  ${LOCAL_DEBUG_CONF_DIR} ]; then
  print_ok "find local_debug conf dir :${LOCAL_DEBUG_CONF_DIR}"
else
  print_error "ERROR: can not found local_debug conf dir :${LOCAL_DEBUG_CONF_DIR}"
  exit 1
fi


print_ok "GO INTO SHELL"
print "shell prepare app view for app instance:${APP_INSTANCE}"

if [ -d ${APP_INSTANCE_VIEWS_DIR} ];then
    print_ok "find views for :${APP_INSTANCE_VIEWS_DIR} , move to tmp dir : instance_views_bak "
    mkdir -p ~/tmp/instance_views_bak
    mv ${APP_INSTANCE_VIEWS_DIR} ~/tmp/instance_views_bak
    
fi
if [ -d ${APP_INSTANCE_VIEWS_DIR} ];then
    print_ok "find views for :${APP_INSTANCE_VIEWS_DIR}"
else
    print "HINT: not find view for:${APP_INSTANCE_VIEWS_DIR} , prepare for it ... ... ..."
    if [ -d ${REPO_INSTANCE_VIEWS_DIR} ];then
        print_ok "OK"  "${APP_INSTANCE} views dir is in gobbs_views"
        print "begin move ${APP_INSTANCE} views dir to "
        
        # rollback by trap
        mv ${REPO_INSTANCE_VIEWS_DIR}  ${APP_INSTANCE_VIEWS_DIR}
        print_ok "begin generate conf dir fils: app.conf and routes"
        print_ok "in DEBUG mode , app.conf do not change , so skip it ."
        print    "generate for routes "
        is_check_app_type_and_instance_name="false"
        python ${ROUTES_GENERATE_ROLLBACK_PY}   ${APP_TYPE}   ${APP_INSTANCE}  "generate" ${is_check_app_type_and_instance_name}
        if [ 0 -eq $? ];then
          print_ok "generate routes ok"
        else
          rollback_views
          print_error "ERROR , when generate routes ."
          print_error "EXIT SHELL , abort."
          exit 1
        fi

    else
        print_error "${REPO_INSTANCE_VIEWS_DIR} "
        print_error "ERROR" "${REPO_INSTANCE_VIEWS_DIR} views dir is not in gobbs_views dir ${REPO_VIEWS_DIR}  "
        print_error "EXIT SHELL , abort"
        exit 1
    fi
fi


if [ -d ${APP_INSTANCE_VIEWS_DIR} ];then
    echo ""
else
    print_error  "NOT FOUND: instance view dir : " " ${APP_INSTANCE_VIEWS_DIR}   "
    exit 1  
fi



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
print_ok "revel run ${APP_TYPE}"

revel run ${APP_TYPE}
# if revel not exist , should rollback

if ! [ $? -eq 0 ];then
  print_error " run error , so rollback"
  sync_views
  print_ok "Done, rollback"
  exit 0
else
  print_ok " run ok ... ... "
fi

sync_views
print_error "EXIT SHELL , unknow status "


