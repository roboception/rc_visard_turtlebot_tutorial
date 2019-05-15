#!/bin/bash


executable=$1

docker run --rm \
	--device=/dev/kobuki:/dev/kobuki \
	--device=/dev/input/js0:/dev/input/js0 \
	 -v ../map:/map:rw \
	--network host \
	turtlebot_image \
	$executable 
