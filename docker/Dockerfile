FROM osrf/ros:kinetic-desktop-full
# FROM ros:kinetic-ros-base

SHELL ["/bin/bash", "-c"]

# gazebo7のリポジトリ追加．新しいやつを入れるため．
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'; \
  apt-get update && apt-get install -y wget; wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add -

# 環境構築インストール
RUN apt-get update && apt-get install --no-install-recommends -y \
  ros-kinetic-turtlebot3-* iputils-ping net-tools gnome-terminal libcanberra-gtk-module libcanberra-gtk3-module dbus-x11 gazebo7\
  && rm -rf /var/lib/apt/lists/*

# burger_war関連のインストール
RUN apt-get update && apt-get install --no-install-recommends -y \
  python-pip ros-kinetic-turtlebot3 ros-kinetic-turtlebot3-msgs ros-kinetic-turtlebot3-simulations ros-kinetic-aruco-ros
RUN pip install requests flask

# burger_warパッケージのセットアップ
RUN source /opt/ros/kinetic/setup.bash
RUN mkdir -p ~/catkin_ws_burger/src
RUN source /opt/ros/kinetic/setup.bash; cd ~/catkin_ws_burger/src;catkin_init_workspace
RUN source /opt/ros/kinetic/setup.bash; cd ~/catkin_ws_burger;catkin_make
RUN cd ~/catkin_ws_burger/src; git clone https://github.com/OneNightROBOCON/burger_war

# nvidia-docker hooks
# LABEL com.nvidia.volumes.needed="nvidia_driver"
# ENV PATH /usr/local/nvidia/bin:${PATH}
# ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}

# .bashrcへの変数追記
RUN echo "export ROS_MASTER_URI=http://172.17.0.1:11311" >> ~/.bashrc
RUN echo "export ROS_IP=\`ifconfig | grep inet | head -1 | cut -d ':' -f 2 | cut -d' ' -f 1\`" >> ~/.bashrc
RUN echo "export GAZEBO_MODEL_PATH=$HOME/catkin_ws_burger/src/burger_war/burger_war/models/" >> ~/.bashrc
RUN echo "source ~/catkin_ws_burger/devel/setup.bash" >> ~/.bashrc
# RUN echo "export ROS_MASTER_URI=http://172.17.0.1:11311"
# RUN echo "export ROS_IP=`ifconfig | grep inet | head -1 | cut -d ':' -f 2 | cut -d' ' -f 1`" >> ~/.bashrc
# RUN echo "source ~/catkin_ws_burger/devel/setup.bash" >> ~/.bashrc
# RUN echo "export GAZEBO_MODEL_PATH=$HOME/catkin_ws_burger/src/burger_war/burger_war/models/" >> ~/.bashrc
# CMD [ "gazebo" ]
