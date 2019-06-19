FROM ros:melodic-ros-core                                                       
MAINTAINER Jan-Niklas Blind <jan-niklas.blind@roboception.de> 

RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

RUN apt-get update && apt-get install -y \
	ros-melodic-desktop-full \
	python-catkin-tools 

RUN mkdir -p /turtlebot_ws/src && cd /turtlebot_ws && \
	/ros_entrypoint.sh catkin init && catkin config --install

COPY . /turtlebot_ws/src/rc_visard_turtlebot_tutorial

RUN cd /turtlebot_ws/src/rc_visard_turtlebot_tutorial/docker && \                                     
	chmod +x .install_turtlebot_docker.sh &&  \ 
	./.install_turtlebot_docker.sh && \                                                     
	cd /turtlebot_ws && \
	/ros_entrypoint.sh rosdep update && rosdep install --from-paths /turtlebot_ws/src/rc_visard_turtlebot_tutorial -y && \
	/ros_entrypoint.sh catkin build && \
	chmod +x /turtlebot_ws/install/share/rc_visard_turtlebot_tutorial/scripts/* && \
	rm -rf /var/lib/apt/lists/*

COPY ./docker/.turtlebot_entrypoint.sh / 

ENTRYPOINT ["/.turtlebot_entrypoint.sh"]
CMD ["bash"]
