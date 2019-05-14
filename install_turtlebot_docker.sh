#!/usr/bin/env sh

cd /turtlebot_ws/src
# copied from turtlebot2_to_melodic repository: https://github.com/gaunthan/Turtlebot2-On-Melodic
### 
git clone https://github.com/turtlebot/turtlebot.git
git clone https://github.com/turtlebot/turtlebot_msgs.git
git clone https://github.com/turtlebot/turtlebot_apps.git
git clone https://github.com/turtlebot/turtlebot_simulator

git clone https://github.com/yujinrobot/kobuki_msgs.git
git clone https://github.com/yujinrobot/kobuki.git
mv kobuki/kobuki_description kobuki/kobuki_node \
  kobuki/kobuki_keyop kobuki/kobuki_safety_controller \
  kobuki/kobuki_bumper2pc ./
rm -rf kobuki

git clone https://github.com/yujinrobot/yujin_ocs.git
mv yujin_ocs/yocs_cmd_vel_mux yujin_ocs/yocs_controllers .
rm -rf yujin_ocs

###

# get laptop_battery_monitor-package
git clone https://github.com/ros-drivers/linux_peripheral_interfaces.git
cd linux_peripheral_interfaces
rm -rf libsensors_monitor
rm -rf linux_peripheral_interfaces

cd /turtlebot_ws
