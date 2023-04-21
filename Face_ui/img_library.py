img_library =  ['66expressionless-face',
                '30partying-face',
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
                '42weary-face']

library =  [[  0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,1, 1,0,0,0, 0,0  ], # 1 Expressionless-face
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,1, 0,0,0,0, 0,0,0,0, 0,1  ], # 2 Partying Face
            [  0,0,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,1, 0,1,0,0, 0,0,0,0, 0,0  ], # 3 Grinning Face with Smiling Eyes
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,0, 0,0,0,0, 0,0  ], # 4 Beaming Face with Smiling Eyes
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0  ], # 5 Smiling Face with Sunglasses
            [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 6 Face with Peeking Eye
            [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 7 Nauseated Face
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 8 Face with Rolling Eyes
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 9 Grinning Squinting Face
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 1,0,0,0, 0,0  ], # 10 Slightly Smiling Face
            [  1,0,0,0, 1,1,0,0, 0,0,0,0, 0,1,0,0, 0,0,1,1, 1,0,0,0, 0,0  ], # 11 Smiling Face with Open Hands
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 0,0,0,0, 0,0  ], # 12 Partying Face
            [  0,0,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 0,0  ], # 13 Smiling Face with Heart-Eyes
            [  1,1,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 1,0,0,0, 0,0  ], # 14 Smiling Face
            [  0,0,0,0, 0,1,0,0, 0,0,0,0, 0,0,0,1, 0,1,0,0, 0,0,1,0, 1,0  ], # 15 Smiling Face with Open Hands
            [  0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1  ], # 16 Zipper-Mouth Face
            [  0,0,0,0, 1,1,0,0, 1,0,0,0, 0,1,0,0, 1,1,0,0, 0,0,0,0, 0,0  ], # 17 Face Blowing a Kiss
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 1,0,0,0, 0,0  ], # 18 Face with Open Mouth
            [  0,0,0,1, 0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 19 Confused Face
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 0,1,0,0, 0,1  ], # 20 Fearful Face
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 21 Smiling Face
            [  0,0,0,1, 0,0,1,0, 0,0,1,1, 0,1,1,0, 1,0,1,0, 0,1,0,0, 0,1  ], # 22 Face Screaming in Fear
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,1,0, 0,1,0,1, 0,0  ], # 23 Face with Open Eyes and Hand Over Mouth
            [  0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 24 Pleading Face
            [  0,1,0,0, 0,0,0,1, 0,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,0, 0,0  ], # 25 Slightly Smiling Face			    
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 26 Thinking Face
            [  0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,0,0, 0,1  ], # 27 Fearful Face
            [  0,0,1,1, 0,0,1,0, 0,1,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 28 Face with Raised Eyebrow
            [  0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,1  ], # 29 Face with Open Mouth
            [  1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 30 Face Without Mouth
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 31 Face Exhaling
            [  0,0,0,0, 1,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 32 Smiling Face with Sunglasses
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,1, 1,0  ], # 33 Disappointed Face
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,1, 1,0,0,1, 1,0,0,0, 0,0  ], # 34 Smiling Face with Halo
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 35 Angry Face
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ], # 36 Relieved Face
            [  0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 37 Drooling Face
            [  0,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 1,0,1,0, 0,0  ], # 38 Smiling Face with Sunglasses
            [  0,1,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 39 Winking Face
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ], # 40 Smiling Face with Sunglasses
            [  0,0,0,0, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 41 Yawning Face
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 1,0,1,0, 0,1  ], # 42 Slightly Smiling Face
            [  1,0,0,0, 1,1,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ]] # 43 Winking Face
     