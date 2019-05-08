#!/usr/bin/env python
"""Simplified script to save the SLAM trajectory into a bagfile from the rc_visard_driver

Calls the ROS service '/rc_visard_driver/get_trajectory' (or the one specified as command line argument
and stores the received nav_msgs/Path into the bagfile 'path.bag' and the trajectory file 'path.txt'
into the current working directory.
"""

from __future__ import print_function

import sys
import rospy
from rc_visard_driver.srv import GetTrajectory
from nav_msgs.msg import Path
import tf2_msgs.msg
import geometry_msgs.msg
import rosbag
import time
import os.path


def copy_with_header_stamp(inbag, outbag):
    # ten times <epoch> (at the time of coding) should be safe for a while
    first_stamp = rospy.Time.from_seconds(15300255090)
    last_stamp = rospy.Time.from_seconds(0)
    msgcount = inbag.get_message_count()
    displaystep = (msgcount / 20)
    if displaystep == 0:
        displaystep = (msgcount / 100)
    if displaystep == 0:
        displaystep = 1
    counter = 0
    for topic, msg, t in inbag.read_messages():
        counter += 1

        # This also replaces tf timestamps under the assumption
        # that all transforms in the message share the same timestamp
        if topic == "/tf" and msg.transforms:
            outbag.write(topic, msg, msg.transforms[0].header.stamp)
            msg_time = msg.transforms[0].header.stamp
        else:
            msg_time = msg.header.stamp if msg._has_header else t
            outbag.write(topic, msg, msg_time)

        if msg_time < first_stamp:
            first_stamp = msg_time
        if msg_time > last_stamp:
            last_stamp = msg_time

        if (counter % displaystep == 0):
            print(counter, "/", msgcount)

    return (first_stamp, last_stamp)


def trajectory_msg_to_tf_bag(outbag, child_frame, trajectory_msg, first_stamp, last_stamp):
    all_poses = 0
    used_poses = 0
    for pose_stamped in trajectory_msg.poses:
        all_poses += 1
        if pose_stamped.header.stamp >= first_stamp and pose_stamped.header.stamp <= last_stamp:
            used_poses += 1
            tfmsg = tf2_msgs.msg.TFMessage()
            tf_transform_stamped = geometry_msgs.msg.TransformStamped()
            tf_transform_stamped.header = pose_stamped.header
            tf_transform_stamped.child_frame_id = child_frame
            tf_transform_stamped.transform.translation.x = pose_stamped.pose.position.x
            tf_transform_stamped.transform.translation.y = pose_stamped.pose.position.y
            tf_transform_stamped.transform.translation.z = pose_stamped.pose.position.z
            tf_transform_stamped.transform.rotation.w = pose_stamped.pose.orientation.w
            tf_transform_stamped.transform.rotation.x = pose_stamped.pose.orientation.x
            tf_transform_stamped.transform.rotation.y = pose_stamped.pose.orientation.y
            tf_transform_stamped.transform.rotation.z = pose_stamped.pose.orientation.z

            tfmsg.transforms.append(tf_transform_stamped)
            outbag.write("/tf", tfmsg, pose_stamped.header.stamp)
    print(used_poses, "of", all_poses, "trajectory poses were in the time frame of the data (ignored the rest).")


def main():
    service_name = '/rc_visard_driver/slam_get_trajectory'

    if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Usage:", sys.argv[0], "input.bag output.bag")
        print()
        print("Requests the trajectory from the rc_visard_driver")
        print("Writes a bag file (tf.bag) with the trajectory poses converted to tf transforms")
        print()
        print("Called service is", service_name)
        sys.exit()

    print("Called service is", service_name)
    input_bagfile_name = sys.argv[1]
    output_bagfile_name = sys.argv[2]

    rospy.init_node("trajectoryServiceClient")
    print("Waiting for service", service_name)
    rospy.wait_for_service(service_name)
    try:
        getTrajectoryProxy = rospy.ServiceProxy(service_name, GetTrajectory)
        print("Calling service ...")
        zero_duration = rospy.Duration()
        response = getTrajectoryProxy(zero_duration, zero_duration, False, False)

        with rosbag.Bag(input_bagfile_name, allow_unindexed=True) as inbag:
            with rosbag.Bag(output_bagfile_name, "w", 'lz4', chunk_threshold=1024 * 1024 * 64) as outbag:
                print("Copying original data (converting the reception timestamps to the header stamps) from", input_bagfile_name, "to", output_bagfile_name)
                first, last = copy_with_header_stamp(inbag, outbag)

                print("Adding trajectory poses as tf messages to", output_bagfile_name)
                trajectory_msg_to_tf_bag(outbag, "camera", response.trajectory, first, last)

                print("Adding trajectory poses as tf messages to", output_bagfile_name)
                trajectory_msg_to_tf_bag(outbag, "camera", response.trajectory, first, last)

                print("Adding trajectory path messages to", output_bagfile_name)
                outbag.write("/rc_visard_driver/trajectory", response.trajectory, last)

                print("Done")

    except rospy.ServiceException, e:
        print("Service call failed: {}".format(e))

if __name__ == "__main__":
    main()
