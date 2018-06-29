#!/usr/bin/env python
"""Script to simplyfiy loading of the previous SLAM map and start SLAM using rc_visard_driver
"""

from __future__ import print_function

import sys
import time
import rospy
from std_srvs.srv import Trigger


def main():
    rospy.init_node("slam_loader")

    service_ns = '/rc_visard_driver'

    # set up services we need
    stop_slam = rospy.ServiceProxy(service_ns + '/dynamics_stop_slam', Trigger)
    reset_slam = rospy.ServiceProxy(service_ns + '/dynamics_reset_slam', Trigger)
    start_slam = rospy.ServiceProxy(service_ns + '/dynamics_start_slam', Trigger)
    load_map = rospy.ServiceProxy(service_ns + '/load_map', Trigger)

    # wait until everthing is available
    rospy.wait_for_service(service_ns + '/dynamics_stop_slam')

    try:
        # first we reset slam (in case it was already running)
        print("stopping SLAM")
        response = stop_slam()
        if not response.success:
            print("failed to stop SLAM: %s" % response.message)
            sys.exit(1)

        print("resetting SLAM")
        response = reset_slam()
        if not response.success:
            print("failed resetting SLAM: %s" % response.message)
            sys.exit(1)

        print("waiting for SLAM to go to idle")
        time.sleep(10)

        # then load the slam map
        print("load SLAM map")
        response = load_map()
        if not response.success:
            print("failed loading SLAM map: %s" % response.message)
            sys.exit(1)

        # then start slam again
        print("starting SLAM")
        response = start_slam()
        if not response.success:
            print("failed starting SLAM: %s" % response.message)
            sys.exit(1)

    except rospy.ServiceException as e:
        print("service call failed: %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()
