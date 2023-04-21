#!/usr/bin/env python3
# import rospy
# from baxter_interface import Limb
# import baxter_interface
import time
import cv2
from numpy import argmax
from numpy import dot
from numpy.linalg import norm
# import cv_bridge
# import rospkg
# from sensor_msgs.msg import Image
import random

from .img_library import library, img_library

def callback(data):
	global msg
	global msg_closed
	if not data == msg_closed:
		msg = data

# rospy.init_node('blinking')

# msg_closed = cv_bridge.CvBridge().cv2_to_imgmsg(img_closed)
# msg = cv_bridge.CvBridge().cv2_to_imgmsg(img)

# pub = rospy.Publisher('/robot/xdisplay', Image,latch=True, queue_size=10)

# while not rospy.is_shutdown():

def main(text_input):
	
	_images = '/home/vboxuser/Voice-Assistant/Face_ui/Faces/'

	print("Library lenght is: ",  len(library))
	list = []
	for i in range(len(library)):
		# counting cosine similarity
		# print(i, "num: ", norm(text_input)*norm(library[i][:]))
		cos_sim = dot(text_input, library[i][:])/(norm(text_input)*norm(library[i][:]))
		list.append(cos_sim)
	
	
	pred = argmax(list, axis = None, out = None)
	print("Hello: ", pred)
	
	print(img_library[pred])
	img = cv2.imread(_images + img_library[pred] + ".png")

	cv2.imshow('Hello', img)
	cv2.waitKey(0)
	# time.sleep(3)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	
	text_input = [  1,0,0,0, 1,1,0,0, 0,0,1,0, 0,1,0,1, 0,0,0,0, 0,1,0,0, 0,1  ]
	main(text_input)