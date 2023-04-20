#!/usr/bin/env python
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

def callback(data):
	global msg
	global msg_closed
	if not data == msg_closed:
		msg = data

# rospy.init_node('blinking')

def smile():
	img = cv2.imread(_images + '/2smiling-face-with-open-mouth-and-smiling-eyes.png')
	# cv2.imshow('Hello', img)
	return img

def sad():
	img = cv2.imread(_images + '/34pensive-face.png')
	# cv2.imshow('Hello', img)
	return img

def angry():
	img = cv2.imread(_images + '/48pouting-face.png')
	# cv2.imshow('Hello', img)
	return img

# msg_closed = cv_bridge.CvBridge().cv2_to_imgmsg(img_closed)
# msg = cv_bridge.CvBridge().cv2_to_imgmsg(img)

# pub = rospy.Publisher('/robot/xdisplay', Image,latch=True, queue_size=10)

# while not rospy.is_shutdown():

def main():
	text_input = [  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ]

	img_library =  ['0grinning-face',
					'1smiling-face-with-open-mouth',
					'2smiling-face-with-open-mouth-and-smiling-eyes',
					'3grinning-face-with-smiling-eyes',
					'4smiling-face-with-open-mouth-and-closed-eyes',
					'5smiling-face-with-open-mouth-and-cold-sweat',
					'6face-with-tears-of-joy',
					'7rolling-on-the-floor-laughing',
					'8smiling-face',
					'9smiling-face-with-smiling-eyes',
					'10smiling-face-with-halo',
					'11slightly-smiling-face',
					'12upside-down-face',
					'13winking-face',
					'14relieved-face',
					'15smiling-face-with-heart-eyes',
					'16smiling-face-with-3-hearts',
					'17face-blowing-a-kiss',
					'18kissing-face-with-smiling-eyes',
					'18kissing-face',
					'19kissing-face-with-closed-eyes',
					'20face-savouring-delicious-food',
					'21face-with-stuck-out-tongue',
					'22face-with-stuck-out-tongue-and-closed-eyes',
					'23face-with-stuck-out-tongue-and-winking-eye',
					'24crazy-face',
					'25face-with-raised-eyebrow',
					'26face-with-monocle',
					'27nerd-face',
					'28smiling-face-with-sunglasses',
					'29star-struck',
					'30partying-face',
					'31smirking-face',
					'32unamused-face',
					'33disappointed-face',
					'34pensive-face',
					'35worried-face',
					'36confused-face',
					'37slightly-frowning-face',
					'38frowning-face',
					'39persevering-face',
					'40confounded-face',
					'41tired-face',
					'42weary-face',
					'43pleading-face',
					'44crying-face',
					'45loudly-crying-face',
					'46face-with-steam-from-nose',
					'47angry-face',
					'48pouting-face',
					'49face-with-symbols-over-mouth',
					'50exploding-head',
					'51flushed-face',
					'52hot-face',
					'53cold-face',
					'54face-screaming-in-fear',
					'55fearful-face',
					'56face-with-open-mouth-and-cold-sweat',
					'57disappointed-but-relieved-face',
					'58face-with-cold-sweat',
					'59hugging-face',
					'60thinking-face',
					'61face-with-hand-over-mouth',
					'62shushing-face',
					'63lying-face',
					'64face-without-mouth',
					'65neutral-face',
					'66expressionless-face',
					'67grimacing-face',
					'68face-with-rolling-eyes',
					'69hushed-face',
					'70frowning-face-with-open-mouth',
					'71anguished-face',
					'72face-with-open-mouth',
					'73astonished-face',
					'74sleeping-face',
					'75drooling-face',
					'76sleepy-face',
					'77dizzy-face',
					'78zipper-mouth-face',
					'79woozy-face',
					'80nauseated-face',
					'81face-vomiting',
					'82sneezing-face',
					'83face-with-thermometer',
					'84face-with-head-bandage',
					'85money-mouth-face',
					'86smiling-face-with-horns',
					'87angry-face-with-horns',
					'88clown-face',
					'89robot-face']

	library =  [[  0, 0, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],			    
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],	
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ],
    			[  1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 1  ]]
	
	_images = '/home/vboxuser/Voice-Assistant/Face_ui/Faces/'

	print("Library lenght is: ",  len(library))
	list = []
	for i in range(len(library)):
		# counting cosine similarity
		cos_sim = dot(text_input, library[i][:])/(norm(text_input)*norm(library[i][:]))
		list.append(cos_sim)
	
	
	pred = argmax(list, axis = None, out = None)
	print("Hello: ", pred)
	
	print(img_library[pred])
	img = cv2.imread(_images + img_library[pred] + ".png")

	cv2.imshow('Hello', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()