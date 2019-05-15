#!/bin/bash
set -e

# setup ros environment
source "/turtlebot_ws/install/setup.bash"
exec "$@"
