#!/bin/bash 

cd $ROS_WORKSPACE

# get turtlebot and kobuki packages
git clone https://github.com/turtlebot/turtlebot.git -b kinetic
git clone https://github.com/turtlebot/turtlebot_apps.git -b indigo
git clone https://github.com/turtlebot/turtlebot_msgs.git -b indigo

git clone https://github.com/yujinrobot/kobuki.git -b kinetic

# get laptop_battery_monitor-package
git clone https://github.com/ros-drivers/linux_peripheral_interfaces.git -b kinetic
cd linux_peripheral_interfaces
rm -rf libsensors_monitor
rm -rf linux_peripheral_interfaces

