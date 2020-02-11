FROM nvidia/opengl:1.1-glvnd-runtime-ubuntu16.04

# サーバを日本に変更
RUN sed -i.org -e 's|ports.ubuntu.com|jp.archive.ubuntu.com|g' /etc/apt/sources.list

# インストールに必要なツールをインストール
RUN apt-get update && apt-get install --no-install-recommends -y \
    lsb-release wget

# ROSのリポジトリを追加
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver 'hkp://ha.pool.sks-keyservers.net:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# gazebo7のリポジトリ追加．新しいやつを入れるため．
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
RUN wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add -


# 環境構築インストール
RUN apt-get update
RUN apt-get install --no-install-recommends -y ros-kinetic-desktop-full
RUN apt-get install --no-install-recommends -y ros-kinetic-turtlebot3-*
RUN apt-get install --no-install-recommends -y iputils-ping
RUN apt-get install --no-install-recommends -y net-tools
RUN apt-get install --no-install-recommends -y gnome-terminal
RUN apt-get install --no-install-recommends -y libcanberra-gtk-module
RUN apt-get install --no-install-recommends -y libcanberra-gtk3-module
RUN apt-get install --no-install-recommends -y dbus-x11
RUN apt-get install --no-install-recommends -y gazebo7
RUN apt-get install --no-install-recommends -y nano
RUN apt-get install --no-install-recommends -y python-rosdep
RUN apt-get install --no-install-recommends -y python-rosinstall-generator
RUN apt-get install --no-install-recommends -y python-wstool
RUN apt-get install --no-install-recommends -y python-rosinstall
RUN apt-get install --no-install-recommends -y build-essential

# burger_war関連のインストール
RUN apt-get install --no-install-recommends -y python-pip
RUN apt-get install --no-install-recommends -y ros-kinetic-turtlebot3
RUN apt-get install --no-install-recommends -y ros-kinetic-turtlebot3-msgs
RUN apt-get install --no-install-recommends -y ros-kinetic-turtlebot3-simulations
RUN apt-get install --no-install-recommends -y ros-kinetic-aruco-ros
RUN pip install requests
RUN pip install flask

# aptキャッシュの削除
RUN apt-get clean; rm -rf /var/lib/apt/lists/*


# .bashrcへの変数追記
# RUN echo "export ROS_MASTER_URI=http://172.17.0.1:11311" >> ~/.bashrc
RUN echo "alias sb='source ~/.bashrc'" >> ~/.bashrc
RUN echo "export ROS_IP=\`ifconfig | grep inet | head -1 | cut -d ':' -f 2 | cut -d' ' -f 1\`" >> ~/.bashrc
RUN echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
RUN echo 'ln -s $ROS_WS /root/' >> ~/.profile
RUN echo 'source $ROS_WS/devel/setup.bash' >> ~/.bashrc
# RUN echo "source /root/catkin_ws/devel/setup.bash" >> ~/.bashrc

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
