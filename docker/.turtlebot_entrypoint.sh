#!/bin/bash
set -e

# setup ros environment
source "/turtlebot_ws/devel/setup.bash"
exec "$@"
