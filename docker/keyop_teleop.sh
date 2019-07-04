#!/bin/bash


docker run --rm \
	-v $(pwd)/map:/map:rw \
	--network host \
	turtlebot_image \
	roslaunch turtlebot_teleop keyboard_teleop.launch
