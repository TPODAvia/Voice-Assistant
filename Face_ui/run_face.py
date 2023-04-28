#!/usr/bin/env python3

import cv2
from numpy import save
from numpy import argmax
from numpy import dot
from numpy.linalg import norm
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Face_ui.img_library import library, img_library

def callback(data):
	global msg
	global msg_closed
	if not data == msg_closed:
		msg = data


def main(text_input):
	
	_images = SCRIPT_DIR + '/Faces/'

	# print("Library lenght is: ",  len(library))
	list = []
	for i in range(len(library)):
		# counting cosine similarity
		# print(i, "num: ", norm(text_input)*norm(library[i][:]))
		cos_sim = dot(text_input, library[i][:])/(norm(text_input)*norm(library[i][:]))
		list.append(cos_sim)
	
	pred = argmax(list, axis = None, out = None)

	emot_convert = pred + 1
	if emot_convert in [22,35]:
		# Angry
		print("Angry")
		save(os.path.dirname(SCRIPT_DIR) + "/Irene-Voice-Assistant/tts_cache/emotts/emotion", 0)

	elif emot_convert in [2,3,4,5,10,11,12,13,14,15,17,21,25,32,34,38,39,40,42,43]:
		# Happy
		print("Happy")
		save(os.path.dirname(SCRIPT_DIR) + "/Irene-Voice-Assistant/tts_cache/emotts/emotion", 1)

	elif emot_convert in [1,26,28,30,36,37]:
		# Neutral
		print("Neutral")
		save(os.path.dirname(SCRIPT_DIR) + "/Irene-Voice-Assistant/tts_cache/emotts/emotion", 2)

	elif emot_convert in [6,7,16,19,24,31,33,41]:
		# Sad
		print("Sad")
		save(os.path.dirname(SCRIPT_DIR) + "/Irene-Voice-Assistant/tts_cache/emotts/emotion", 3)

	elif emot_convert in [8,18,20,23,27,29]:
		# Surprise
		print("Surprise")
		save(os.path.dirname(SCRIPT_DIR) + "/Irene-Voice-Assistant/tts_cache/emotts/emotion", 4)

	# print(img_library[pred])
	img = cv2.imread(_images + img_library[pred] + ".png")

	return img

if __name__ == '__main__':
	
	text_input = [  0,2,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ]
	img = main(text_input)

	cv2.imshow('Hello', img)

	while True:
		k = cv2.waitKey(33)
		if k==27:    # Esc key to stop
			break