#!/usr/bin/env python
# import rospy
# from baxter_interface import Limb
# import baxter_interface
import time
import cv2
# import cv_bridge
# import rospkg
# from sensor_msgs.msg import Image
import random



def callback(data):
	global msg
	global msg_closed
	if not data == msg_closed:
		msg = data

# rospy.init_node('blinking')

_images = '/home/vboxuser/Voice-Assistant/baxter-eyes'
img = cv2.imread(_images + '/straight.jpg')
# sub = rospy.Subscriber('/robot/xdisplay', Image, callback)
img_closed = cv2.imread(_images + '/closed.jpg')

# msg_closed = cv_bridge.CvBridge().cv2_to_imgmsg(img_closed)
# msg = cv_bridge.CvBridge().cv2_to_imgmsg(img)

# pub = rospy.Publisher('/robot/xdisplay', Image,latch=True, queue_size=10)

# while not rospy.is_shutdown():
while True:
	timer = random.randint(2,4)	
	cv2.imshow('Hello', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	time.sleep(timer)
	print("blinking")
	# pub.publish(msg_closed)
	# pub.publish(msg)
