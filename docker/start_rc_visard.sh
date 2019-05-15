#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <rc_visard serial number"
	exit 1
fi

serial_number=$1

docker run --rm \
	--network host \
	turtlebot_image \
	rosrun rc_visard_driver rc_visard_driver _device:=:$serial_number _autostart_dynamics:=True _autostart_dynamics_with_slam:=True _autostop_dynamics:=True _autopublish_trajectory:=True _enable_tf:=True
