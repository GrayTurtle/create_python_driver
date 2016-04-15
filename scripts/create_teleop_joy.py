#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Empty

MAXLINEAR = 1
MAXANGULAR = 3
linear = 0

class MyClass:
	
	def __init__(self):
		rospy.init_node('create_teleop')
		self.pub = rospy.Publisher("Create2_Driver/cmd_vel", Twist, queue_size=5)
		self.pubStop = rospy.Publisher("Create2_Driver/stop", Empty, queue_size=1)
		self.pubReset = rospy.Publisher("Create2_Driver/reset", Empty, queue_size=1)
	
	def callback(self,msg):
		command = Twist()
		linear = 0
		if msg.buttons[1] == 1:
			direction = -1
		else:
			direction = 1
		
		if msg.buttons[7] == 1:
			linear = direction*MAXLINEAR
	
		if msg.buttons[9] == 1:
			self.pubReset.publish()
		if msg.buttons[8] == 1:
			self.pubStop.publish()
		angular = msg.axes[0]*MAXANGULAR
		command.linear.x = linear
		command.angular.z = angular		
		self.pub.publish(command)
		print angular
		print linear

		'''
		axis[0] left and right pos and neg
		axis[1] up and down pos and neg
		button[7] throttle
		button[1] reverse
		button[9] enable and disable
		'''

if __name__=="__main__":
    my = MyClass()
    rospy.Subscriber("/joy", Joy, my.callback)
    rospy.spin()
