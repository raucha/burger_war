#!/bin/bash

# set default level 1
VALUE_L="3"
# set default color red
VALUE_SIDE="r"

# get args level setting
while getopts ls: OPT
do
  case $OPT in
    "l" ) FLG_L="TRUE" ; VALUE_L="$OPTARG" ;;
    "s" ) FLG_S="TRUE"  ; VALUE_SIDE="$OPTARG" ;;
  esac
done

# set judge server state "running"
bash judge/test_scripts/set_running.sh localhost:5000

# launch robot control node
# launch robot control node
# roslaunch burger_war sim_robot_run.launch
# roslaunch burger_war sim_level_1_cheese.launch
# roslaunch burger_war sim_level_2_teriyaki.launch
# roslaunch burger_war sim_level_3_clubhouse.launch
# roslaunch burger_war sim_robot_run.launch enemy_level:=$VALUE_L
roslaunch burger_war sim_robot_run.launch enemy_level:=$VALUE_L _side:=$VALUE_SIDE