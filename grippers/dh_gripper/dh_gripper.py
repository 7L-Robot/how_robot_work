#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import rospy

from dh_gripper_msgs.msg import GripperCtrl

class DH_Gripper():
	def __init__(self):
		self.pub = rospy.Publisher('/gripper/ctrl', GripperCtrl, queue_size=20)
		rospy.sleep(1)

	def control(self, value, sleep=1):
		rospy.loginfo(value)
		ctrl = GripperCtrl()
		ctrl.position = value

		self.pub.publish(ctrl)
		rospy.sleep(sleep)

	def close(self):
		self.control(0, 2)

	def open(self):
		self.control(100, 1)

if __name__ == '__main__':
    
	rospy.init_node('dh_test', anonymous=True)

	gripper = DH_Gripper()

	gripper.open()
	gripper.close()

	rospy.sleep(2)

	gripper.open()
	rospy.sleep(2)
	gripper.close()


# https://github.com/Robotics-Innovations-Lab/AG95-ROS/tree/master