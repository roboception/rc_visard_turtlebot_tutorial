#!/bin/bash


docker run --rm \
	--device=/dev/kobuki:/dev/kobuki \
	-v $(pwd)/map:/map:rw \
	--network host \
	turtlebot_image \
	roslaunch turtlebot_bringup minimal.launch 
