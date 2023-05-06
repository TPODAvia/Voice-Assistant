img_library =  ['Happy',
                'Happy',
                'Funny',
                'Funny',
                'Gangsta',
                'Ashamed',
                'Sick',
                'Confuse',
                'Funny',
                'Happy',
                'Happy',
                'Happy',
                'Love',
                'Happy',
                'Happy',
                'Ashamed',
                'Love',
                'Surprise',
                'Confuse',
                'Worry',
                'Happy',
                'Worry',
                'Happy',
                'Scary',
                'Surprise',
                'Pleasing',
                'Happy',
                'Confuse',
                'Surprise',
                'Robot',
                'Sleepy',
                'Gangsta',
                'Sad',
                'Proud',
                'Angry',
                'Proud',
                'Wow',
                'Gangsta',
                'Wrinking',
                'Gangsta',
                'Sad',
                'Happy',
                'Wrinking']
             
library =  [[  0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,1, 1,0,0,0, 0,0  ], # 1 Expressionless-face                      -- Happy
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,1, 0,0,0,0, 0,0,0,0, 0,1  ], # 2 Partying Face                            -- Happy
            [  0,0,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,1, 0,1,0,0, 0,0,0,0, 0,0  ], # 3 Grinning Face with Smiling Eyes          -- Funny
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,0, 0,0,0,0, 0,0  ], # 4 Beaming Face with Smiling Eyes           -- Funny
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0  ], # 5 Smiling Face with Sunglasses             -- Gangsta
            [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 6 Face with Peeking Eye                    -- Ashamed
            [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 7 Nauseated Face                           -- Sick
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 8 Face with Rolling Eyes                   -- Confuse
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 9 Grinning Squinting Face                  -- Funny
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 1,0,0,0, 0,0  ], # 10 Slightly Smiling Face                   -- Happy
            [  1,0,0,0, 1,1,0,0, 0,0,0,0, 0,1,0,0, 0,0,1,1, 1,0,0,0, 0,0  ], # 11 Smiling Face with Open Hands            -- Happy
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 0,0,0,0, 0,0  ], # 12 Partying Face                           -- Happy
            [  0,0,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 0,0  ], # 13 Smiling Face with Heart-Eyes            -- Love
            [  1,1,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 1,0,0,0, 0,0  ], # 14 Smiling Face                            -- Happy
            [  0,0,0,0, 0,1,0,0, 0,0,0,0, 0,0,0,1, 0,1,0,0, 0,0,1,0, 1,0  ], # 15 Smiling Face with Open Hands            -- Happy
            [  0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1  ], # 16 Zipper-Mouth Face                       -- Ashamed
            [  0,0,0,0, 1,1,0,0, 1,0,0,0, 0,1,0,0, 1,1,0,0, 0,0,0,0, 0,0  ], # 17 Face Blowing a Kiss                     -- Love
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 1,0,0,0, 0,0  ], # 18 Face with Open Mouth                    -- Surprise
            [  0,0,0,1, 0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 19 Confused Face                           -- Confuse
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 0,1,0,0, 0,1  ], # 20 Fearful Face                            -- Worry
            [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 21 Smiling Face                            -- Happy
            [  0,0,0,1, 0,0,1,0, 0,0,1,1, 0,1,1,0, 1,0,1,0, 0,1,0,0, 0,1  ], # 22 Face Screaming in Fear                  -- Scary
            [  0,1,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,1,0, 0,1,0,1, 0,0  ], # 23 Face with Open Eyes and Hand Over Mouth -- Surprise
            [  0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 24 Pleading Face                           -- Pleading
            [  0,1,0,0, 0,0,0,1, 0,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,0, 0,0  ], # 25 Slightly Smiling Face                   -- Happy
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 26 Thinking Face                           -- Confuse
            [  0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,0,0, 0,1  ], # 27 Fearful Face                            -- Scary
            [  0,0,1,1, 0,0,1,0, 0,1,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 28 Face with Raised Eyebrow                -- Confuse
            [  0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,1  ], # 29 Face with Open Mouth                    -- Surprise
            [  1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 30 Face Without Mouth                      -- Robot
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 31 Face Exhaling                           -- Sleepy
            [  0,0,0,0, 1,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 32 Smiling Face with Sunglasses            -- Gangsta
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,1, 1,0  ], # 33 Disappointed Face                       -- Sad
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,1, 1,0,0,1, 1,0,0,0, 0,0  ], # 34 Smiling Face with Halo                  -- Proud
            [  0,0,0,1, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 35 Angry Face                              -- Angry
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ], # 36 Relieved Face                           -- Proud
            [  0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 37 Drooling Face                           -- Wow
            [  0,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 1,0,1,0, 0,0  ], # 38 Smiling Face with Sunglasses            -- Gangsta
            [  0,1,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 39 Winking Face                            -- Wrinking
            [  0,0,0,0, 0,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ], # 40 Smiling Face with Sunglasses            -- Gangsta
            [  0,0,0,0, 0,0,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ], # 41 Yawning Face                            -- Sad
            [  1,0,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 1,0,0,1, 1,0,1,0, 0,1  ], # 42 Slightly Smiling Face                   -- Happy
            [  1,0,0,0, 1,1,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,0,0, 0,0  ]] # 43 Winking Face                            -- Wrinking
     