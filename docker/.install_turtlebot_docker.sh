#!/bin/bash

cd /turtlebot_ws/src

# get turtlebot and kobuki packages
git clone https://github.com/turtlebot/turtlebot.git
git clone https://github.com/turtlebot/turtlebot_apps.git
git clone https://github.com/turtlebot/turtlebot_msgs.git

git clone https://github.com/yujinrobot/kobuki.git

# get laptop_battery_monitor-package
git clone https://github.com/ros-drivers/linux_peripheral_interfaces.git
cd linux_peripheral_interfaces
rm -rf libsensors_monitor
rm -rf linux_peripheral_interfaces

cd /turtlebot_ws
