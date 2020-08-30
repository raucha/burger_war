#!/bin/bash

xhost +local:root

docker exec -it \
--env="DISPLAY"  \
--env="QT_X11_NO_MITSHM=1"  \
--env="ROS_WS=$HOME/catkin_ws" \
--env="TURTLEBOT3_MODEL" \
--env="GAZEBO_MODEL_PATH" \
--env="ROS_MASTER_URI" \
--workdir="$HOME" \
-e LOCAL_USER_ID=`id -u $USER` \
-e LOCAL_GROUP_ID=`id -g $USER` \
-e LOCAL_GROUP_NAME=`id -gn $USER` \
 burger_war_container bash -i -c 'cd $ROS_WS/src/burger_war; bash scripts/start.sh -l 1 -s b'

xhost -local:root
