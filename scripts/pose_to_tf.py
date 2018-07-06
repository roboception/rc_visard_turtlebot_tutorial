#!/usr/bin/env python
import rospy
import sys
import tf2_msgs.msg
import geometry_msgs.msg
import argparse

def invertPose(p):
    import tf.transformations as tfs
    T = tfs.quaternion_matrix([p.orientation.x, p.orientation.y, p.orientation.z, p.orientation.w])
    T[0:3,3] = [ p.position.x, p.position.y, p.position.z ]
    T_inv = tfs.inverse_matrix(T)
    q = tfs.quaternion_from_matrix(T_inv)
    p.orientation.x = q[0]
    p.orientation.y = q[1]
    p.orientation.z = q[2]
    p.orientation.w = q[3]
    p.position.x = T_inv[0,3]
    p.position.y = T_inv[1,3]
    p.position.z = T_inv[2,3]

def main():
    parser = argparse.ArgumentParser(description='''This script converts PoseStamped to TFMessage.''')
    parser.add_argument('-it','--input_topic', help='The input pose topic', default='/pose')
    parser.add_argument('-c', '--child_frame_id', help='Set this as the child frame (default: "camera")', default="camera")
    parser.add_argument('-p', '--parent_frame_id', help='Set this as parent frame (default: take frame_id of input pose', default=None)
    parser.add_argument('-i', '--invert', action="store_true", help='Invert the transformation (make sure to set child and parent accordingly)')
    args = parser.parse_args(rospy.myargv()[1:])
    pub = rospy.Publisher('/tf', tf2_msgs.msg.TFMessage, queue_size=10)
    rospy.init_node('pose_conversion', anonymous=True)

    def pose_callback(pose_stamped):
        tfmsg = tf2_msgs.msg.TFMessage()
        tf_transform_stamped = geometry_msgs.msg.TransformStamped()
        tf_transform_stamped.header = pose_stamped.header
        if args.parent_frame_id != None:
          tf_transform_stamped.header.frame_id = args.parent_frame_id

        p = pose_stamped.pose
        if args.invert:
          invertPose(p)

        tf_transform_stamped.child_frame_id = args.child_frame_id
        tf_transform_stamped.transform.translation.x = p.position.x
        tf_transform_stamped.transform.translation.y = p.position.y
        tf_transform_stamped.transform.translation.z = p.position.z
        tf_transform_stamped.transform.rotation.w = p.orientation.w
        tf_transform_stamped.transform.rotation.x = p.orientation.x
        tf_transform_stamped.transform.rotation.y = p.orientation.y
        tf_transform_stamped.transform.rotation.z = p.orientation.z

        tfmsg.transforms.append(tf_transform_stamped)
        pub.publish(tfmsg)

    rospy.Subscriber(args.input_topic, geometry_msgs.msg.PoseStamped, pose_callback)
    rospy.loginfo("Subscribed to " + args.input_topic)
    rospy.spin()

if __name__ == "__main__":
    print sys.argv
    main()
