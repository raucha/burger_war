#!/bin/bash
xhost +local:root

# docker run -it \
docker run -it \
--env="DISPLAY"  \
--env="QT_X11_NO_MITSHM=1"  \
--env="TURTLEBOT3_MODEL=burger" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
--workdir="/home/$USER" \
--volume="/etc/group:/etc/group:ro" \
--volume="/etc/passwd:/etc/passwd:ro" \
--volume="/etc/shadow:/etc/shadow:ro" \
--volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
--volume="$HOME/host_docker:/home/user/host_docker" \
-e LOCAL_USER_ID=`id -u $USER` \
-e LOCAL_GROUP_ID=`id -g $USER` \
-e LOCAL_GROUP_NAME=`id -gn $USER` \
 buger_war
#  buger_war /bin/bash -c "source ~/.bashrc; source ~/catkin_ws_burger/devel/setup.bash ;roslaunch /root/catkin_ws_burger/src/burger_war/burger_war/launch/setup_sim.launch"
#  buger_war /bin/bash -c "source /ros_entrypoint.sh; source ~/.bashrc; roslaunch burger_war setup_sim.launch"
#  buger_war /bin/bash -c "source /ros_entrypoint.sh; roscd buger_war; pwd; ls;bash"
#  buger_war roslaunch burger_war setup_sim.launch
#  buger_war /bin/bash -c "roslaunch burger_war setup_sim.launch"
#  buger_war bash /root/catkin_ws_burger/src/burger_war/scripts/sim.sh

xhost -local:root

# --env="ROS_MASTER_URI=http://172.17.0.1:11311" \
# --env="ROS_IP=`ifconfig | grep inet | head -1 | cut -d ':' -f 2 | cut -d' ' -f 1`" \
# --volume="/home/$USER:/home/$USER" \
#  (roslaunch turtlebot3_gazebo turtlebot3_world.launch)
# export ROS_IP=`ifconfig | grep inet | head -1 | cut -d ':' -f 2 | cut -d' ' -f 1`
