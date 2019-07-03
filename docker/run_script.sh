#!/bin/bash


executable=$1

docker run --rm \
	-v $(pwd)/map:/map:rw \
	--network host \
	turtlebot_image \
	$executable 
