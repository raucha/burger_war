#!/bin/bash

# if docker ps --format '{{.Names}}' | grep -q burger_war_container; then
#     cmd="exec"
# else
#     cmd="run"
# fi
docker rm burger_war_container

xhost +local:root

docker run -it \
--gpus all \
--env="DISPLAY"  \
--env="QT_X11_NO_MITSHM=1"  \
--env="ROS_WS=$HOME/catkin_ws" \
--env="TURTLEBOT3_MODEL" \
--env="GAZEBO_MODEL_PATH" \
--env="ROS_MASTER_URI" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
--workdir="$HOME" \
--volume="/etc/group:/etc/group:ro" \
--volume="/etc/passwd:/etc/passwd:ro" \
--volume="/etc/shadow:/etc/shadow:ro" \
--volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
--volume="$HOME/host_docker:/home/user/host_docker" \
--volume="$HOME/catkin_ws:$HOME/catkin_ws" \
--volume="$HOME/.gazebo:/root/.gazebo" \
-e LOCAL_USER_ID=`id -u $USER` \
-e LOCAL_GROUP_ID=`id -g $USER` \
-e LOCAL_GROUP_NAME=`id -gn $USER` \
--name burger_war_container \
 ros_kinetic_gpu bash -i -c 'cd $ROS_WS/src/burger_war; bash scripts/sim_with_judge.sh -s b'

xhost -local:root
