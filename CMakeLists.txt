cmake_minimum_required(VERSION 2.8.3)

# Don't set PROJECT_VERSION to empty string when no VERSION is given to project() command.
if(POLICY CMP0048)
  cmake_policy(SET CMP0048 OLD)
endif()

project(rc_visard_turtlebot_tutorial)
#include(cmake/project_version.cmake)

find_package(catkin REQUIRED COMPONENTS)

catkin_package()

install(FILES
  launch/turtlebot_driver.launch
  launch/rc_visard_turtlebot_tutorial.launch
  launch/octomap_mapping.launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

install(FILES
  robots/kobuki_hexagons_rc_visard_160.urdf.xacro
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/robots
)

install(FILES
  cfg/rc_visard_costmap_params.yaml
  cfg/navigation_app.rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/cfg
)


install(FILES
  scripts/reset_slam_and_load_map.py
  scripts/save_trajectory_as_tf.py
  scripts/pose_to_tf.py
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/scripts
)

######################################
## Define information for packaging ##
######################################
# optionally specify dependencies of the debian package here (comma separated!)
#set(CPACK_DEBIAN_PACKAGE_DEPENDS "cvkit (>= 1.7.0), ros-$ENV{ROS_DISTRO}-rc-imagecommon")
#include(cmake/package_debian.cmake)
