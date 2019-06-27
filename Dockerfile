FROM ros:melodic-ros-base
MAINTAINER Jan-Niklas Blind <jan-niklas.blind@roboception.de> 

RUN mkdir -p /turtlebot_ws/src 

COPY . /turtlebot_ws/src/rc_visard_turtlebot_tutorial

RUN cd /turtlebot_ws/src/rc_visard_turtlebot_tutorial/docker && \
	chmod +x .install_turtlebot_docker.sh &&  \ 
	./.install_turtlebot_docker.sh && \                                                     
	cd /turtlebot_ws && \
	apt-get update && \
	/ros_entrypoint.sh rosdep update && rosdep install --from-paths /turtlebot_ws/src/ -r -y && \
	/ros_entrypoint.sh catkin_make install && \
	rm -rf /var/lib/apt/lists/*

COPY ./docker/.turtlebot_entrypoint.sh / 

ENTRYPOINT ["/.turtlebot_entrypoint.sh"]
CMD ["bash"]
