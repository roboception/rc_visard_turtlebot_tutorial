#!/bin/bash 

mkdir -p /home/$USER/turtlebot_ws/src
cd /home/$USER/turtlebot_ws
catkin config --init --install
cd src
mv /home/$USER/rc_visard_turtlebot_tutorial /home/$USER/turtlebot_ws/src

# get turlebot packages
git clone https://github.com/turtlebot/turtlebot.git                               
git clone https://github.com/turtlebot/turtlebot_apps.git                          
git clone https://github.com/turtlebot/turtlebot_msgs.git                          
                                                                                   
git clone https://github.com/yujinrobot/kobuki.git                                 
                                                                                   
# get laptop_battery_monitor-package
git clone https://github.com/ros-drivers/linux_peripheral_interfaces.git
cd linux_peripheral_interfaces
rm -rf libsensors_monitor
rm -rf linux_peripheral_interfaces

cd /home/$USER/turtlebot_ws
rosdep update && rosdep install --from-paths src/rc_visard_turtlebot_tutorial -y
catkin build
source install/setup.bash
chmod +x install/share/rc_visard_turtlebot_tutorial/scripts/*
