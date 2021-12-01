#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from fcf import follower


cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
rospy.init_node('red_light_green_light')

red_light_twist = Twist()
green_light_twist =Twist()
green_light_twist.linear.x = 1

driving_forward = False

light_change_time = rospy.Time.now()
rate = rospy.Rate(10)
while not rospy.is_shutdown():
    if driving_forward:
        cmd_vel_pub.publish(green_light_twist)
    else:
        cmd_vel_pub.publish(red_light_twist)
    if rospy.Time.now() > light_change_time:
        driving_forward = not driving_forward
        light_change_time = rospy.Time.now() + rospy.Duration(0.1)
    rate.sleep()