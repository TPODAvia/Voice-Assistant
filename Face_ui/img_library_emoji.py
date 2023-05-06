img_library =  ['66expressionless-face',
                '30partying-face',
                '2smiling-face-with-open-mouth-and-smiling-eyes',
                '3grinning-face-with-smiling-eyes',
                '28smiling-face-with-sunglasses',
                '21face-with-stuck-out-tongue',
                '80nauseated-face',
                '68face-with-rolling-eyes',
                '4smiling-face-with-open-mouth-and-closed-eyes',
                '11slightly-smiling-face',
                '59hugging-face',
                '30partying-face',
                '15smiling-face-with-heart-eyes',
                '8smiling-face',
                '59hugging-face',
                '78zipper-mouth-face',
                '17face-blowing-a-kiss',
                '72face-with-open-mouth',
                '36confused-face',
                '55fearful-face',
                '8smiling-face',
                '54face-screaming-in-fear',
                '69hushed-face',
                '43pleading-face',
                '11slightly-smiling-face',
                '60thinking-face',
                '55fearful-face',
                '25face-with-raised-eyebrow',
                '72face-with-open-mouth',
                '64face-without-mouth',
                '76sleepy-face',
                '28smiling-face-with-sunglasses',
                '33disappointed-face',
                '10smiling-face-with-halo',
                '47angry-face',
                '14relieved-face',
                '75drooling-face',
                '28smiling-face-with-sunglasses',
                '13winking-face',
                '28smiling-face-with-sunglasses',
                '74sleeping-face',
                '11slightly-smiling-face',
                '13winking-face']
             
library =  [[  0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,1, 1,0,0,0, 0,0  ], # 1 Expressionless-face                      -- 66expressionless-face
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,1, 0,0,0,0, 0,0,0,0, 0,1  ], # 2 Partying Face                            -- 30partying-face
            [  0,0,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,1, 0,1,0,0, 0,0,0,0, 0,0  ], # 3 Grinning Face with Smiling Eyes          -- 2smiling-face-with-open-mouth-and-smiling-eyes
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,0, 0,0,0,0, 0,0  ], # 4 Beaming Face with Smiling Eyes           -- 3grinning-face-with-smiling-eyes
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0  ], # 5 Smiling Face with Sunglasses             -- 28smiling-face-with-sunglasses
            [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 6 Face with Peeking Eye                    -- 21face-with-stuck-out-tongue
            [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 7 Nauseated Face                           -- 80nauseated-face
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 8 Face with Rolling Eyes                   -- 68face-with-rolling-eyes
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 9 Grinning Squinting Face                  -- 4smiling-face-with-open-mouth-and-closed-eyes
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 1,0,0,0, 0,0  ], # 10 Slightly Smiling Face                   -- 11slightly-smiling-face
            [  1,0,0,0, 1,1,0,0, 0,0,0,0, 0,1,0,0, 0,0,1,1, 1,0,0,0, 0,0  ], # 11 Smiling Face with Open Hands            -- 59hugging-face
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 0,0,0,0, 0,0  ], # 12 Partying Face                           -- 30partying-face.
            [  0,0,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 0,0  ], # 13 Smiling Face with Heart-Eyes            -- 15smiling-face-with-heart-eyes
            [  1,1,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 1,0,0,0, 0,0  ], # 14 Smiling Face                            -- 8smiling-face
            [  0,0,0,0, 0,1,0,0, 0,0,0,0, 0,0,0,1, 0,1,0,0, 0,0,1,0, 1,0  ], # 15 Smiling Face with Open Hands            -- 59hugging-face
            [  0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1  ], # 16 Zipper-Mouth Face                       -- 78zipper-mouth-face
            [  0,0,0,0, 1,1,0,0, 1,0,0,0, 0,1,0,0, 1,1,0,0, 0,0,0,0, 0,0  ], # 17 Face Blowing a Kiss                     -- 17face-blowing-a-kiss
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 1,0,0,0, 0,0  ], # 18 Face with Open Mouth                    -- 72face-with-open-mouth
            [  0,0,0,1, 0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 19 Confused Face                           -- 36confused-face
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 0,1,0,0, 0,1  ], # 20 Fearful Face                            -- 55fearful-face
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 21 Smiling Face                            -- 8smiling-face
            [  0,0,0,1, 0,0,1,0, 0,0,1,1, 0,1,1,0, 1,0,1,0, 0,1,0,0, 0,1  ], # 22 Face Screaming in Fear                  -- 54face-screaming-in-fear
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,1,0, 0,1,0,1, 0,0  ], # 23 Face with Open Eyes and Hand Over Mouth -- 69hushed-face
            [  0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 24 Pleading Face                           -- 43pleading-face
            [  0,1,0,0, 0,0,0,1, 0,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,0, 0,0  ], # 25 Slightly Smiling Face                   -- 11slightly-smiling-face
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 26 Thinking Face                           -- 60thinking-face
            [  0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,0,0, 0,1  ], # 27 Fearful Face                            -- 55fearful-face
            [  0,0,1,1, 0,0,1,0, 0,1,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 28 Face with Raised Eyebrow                -- 25face-with-raised-eyebrow
            [  0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,1  ], # 29 Face with Open Mouth                    -- 72face-with-open-mouth
            [  1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 30 Face Without Mouth                      -- 64face-without-mouth
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 31 Face Exhaling                           -- 76sleepy-face
            [  0,0,0,0, 1,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 32 Smiling Face with Sunglasses            -- 28smiling-face-with-sunglasses
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,1, 1,0  ], # 33 Disappointed Face                       -- 33disappointed-face
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,1, 1,0,0,1, 1,0,0,0, 0,0  ], # 34 Smiling Face with Halo                  -- 10smiling-face-with-halo
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 35 Angry Face                              -- 47angry-face
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ], # 36 Relieved Face                           -- 14relieved-face
            [  0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 37 Drooling Face                           -- 75drooling-face
            [  0,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 1,0,1,0, 0,0  ], # 38 Smiling Face with Sunglasses            -- 28smiling-face-with-sunglasses
            [  0,1,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 39 Winking Face                            -- 13winking-face
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ], # 40 Smiling Face with Sunglasses            -- 28smiling-face-with-sunglasses
            [  0,0,0,0, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 41 Yawning Face                            -- 74sleeping-face
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 1,0,1,0, 0,1  ], # 42 Slightly Smiling Face                   -- 11slightly-smiling-face
            [  1,0,0,0, 1,1,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ]] # 43 Winking Face                            -- 13winking-face
     