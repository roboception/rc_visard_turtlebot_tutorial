#!/bin/bash

# run docker image with all options                                             
# docker run --name turtlebot --rm \                    
# -v $(pwd)/catkin_entrypoint.sh:/catkin_entrypoint:x \                                       
# --network=host \                                                                
# test_image

executable=$1
# param1=$2
# param2=$3

docker run --rm \
	--device=/dev/kobuki:/dev/kobuki \
	--device=/dev/input/js0:/dev/input/js0 \
	 -v $(pwd)/map:/map:rw \
	--network host \
	turtlebot_image \
	$executable 
	# $executable $param1 $param2

	# --volume $(pwd)/catkin_entrypoint.sh:/root:rw  \

	# source catkin_ws/devel/setup.bash \
