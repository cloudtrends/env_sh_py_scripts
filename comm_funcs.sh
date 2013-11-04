#!/bin/bash


# scriptname - description of script
# http://linuxtidbits.wordpress.com/2008/08/11/output-color-on-bash-scripts/
# Text color variables
txtund=$(tput sgr 0 1)          # Underline
txtbld=$(tput bold)             # Bold
bldred=${txtbld}$(tput setaf 1) #  red
bldblu=${txtbld}$(tput setaf 4) #  blue
bldwht=${txtbld}$(tput setaf 7) #  white
txtrst=$(tput sgr0)             # Reset
info=${bldwht}*${txtrst}        # Feedback
pass=${bldblu}*${txtrst}
warn=${bldred}*${txtrst}
ques=${bldblu}?${txtrst}

function print_ok(  ){
    echo "$(tput setaf 2) $1 $(tput sgr0) $2"
}

function print_error(  ){
    echo "$(tput setaf 1) $1 $(tput sgr0) $2"
}

function print(){
    echo $1 $2
}
