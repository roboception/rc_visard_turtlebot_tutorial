#!/bin/bash


docker run --rm \
	--device=/dev/kobuki:/dev/kobuki \
	--device=/dev/input/js0:/dev/input/js0 \
	-v $(pwd)/map:/map:rw \
	--network host \
	turtlebot_image \
	roslaunch turtlebot_teleop ps3_teleop.launch
