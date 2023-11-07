import pygame
import random
import threading
import sys
import signal


def game_loop():
    tear_Ys = []
    mouth_wide = 700
    mouth_height = 75
    speak = ''
    disabled = False
    #0 = full left and 40 = full right
    eyes_up = 20
    eyes = 20

    # How closed are the eyelids?
    eyelids = 5

    # Automated eyelid animation.  If this list isn't empty, it's the values
    # which we want the 'eyelids' variable to have in each frame.
    eyelid_auto_values = []

    # Automated random blinking?
    auto_blink = False

    finished = False

    player_speak = ''



    pygame.init()
    myfont = pygame.font.SysFont("monospace", 15)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))

    speech_from_key = {pygame.K_t: 'WAA(cry)',
                    pygame.K_h: 'hello',
                    pygame.K_z: 'My',
                    pygame.K_x: 'name',
                    pygame.K_c: 'is',
                    pygame.K_v: 'John',
                    pygame.K_b: 'Paul',
                    pygame.K_n: 'Sparki',
                    pygame.K_j: '<press "y" to write your own speech>'}

    while not finished:
        clock.tick(30)
        for event in pygame.event.get():
                
            if event.type == pygame.QUIT:
                finished = True
            #
            elif event.type == pygame.KEYDOWN:
                if not disabled:
                    if event.key == pygame.K_t:
                        if len(tear_Ys) == 0 or tear_Ys[-1] > 150:
                            tear_Ys.append(100)
                    if event.key == pygame.K_q:
                        auto_blink = not auto_blink
                    if event.key == pygame.K_y:
                        disabled = True
                        player_speak = ''
                else:
                    if event.key == pygame.K_RETURN:
                        speech_from_key[pygame.K_j] = player_speak
                        disabled = False
                    elif event.key == pygame.K_BACKSPACE:
                        # Only makes sense to backspace if there's at least one
                        # character in the speech so far:
                        if len(player_speak) > 0:
                            # If so, take everything except the last character and
                            # make that the new 'player_speak':
                            player_speak = player_speak[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        player_speak = ''
                    else:
                        player_speak += event.unicode

        draw_snot = False

        keys = pygame.key.get_pressed()

        if not disabled:
            if keys[pygame.K_r]:
                # open eyelids
                eyelids -= 5
            if eyelids < 5: eyelids = 5

            if keys[pygame.K_f]:
                # close eyelids
                eyelids += 5
            if eyelids > 60: eyelids = 60

            if keys[pygame.K_e] or (auto_blink and random.randint(1, 120) == 1):
                if not eyelid_auto_values:
                    eyelid_auto_values = [5, 10, 20, 30, 40, 50, 60, 50, 40, 30, 20, 10, 5]
                    while eyelid_auto_values[0] < eyelids:
                        del eyelid_auto_values[0]

            if keys[pygame.K_a]:
                eyes -=3
            if eyes < 0: eyes = 0

            if keys[pygame.K_d]:
                eyes +=3
            if eyes > 40: eyes = 40

            if keys[pygame.K_s]:
                eyes_up +=3
            if eyes_up >40: eyes_up = 40

            if keys[pygame.K_w]:
                eyes_up -=3
            if eyes_up < 0: eyes_up = 0

            if keys[pygame.K_DOWN]:
                mouth_height +=10
            if mouth_height > 120: mouth_height = 120

            if keys[pygame.K_UP]:
                mouth_height -=10
            if mouth_height < 5: mouth_height = 5

            if keys[pygame.K_LEFT]:
                mouth_wide +=10
            if mouth_wide > 700: mouth_wide = 700

            if keys[pygame.K_RIGHT]:
                mouth_wide -=10
            if mouth_wide < 45: mouth_wide = 45

            if keys[pygame.K_SPACE]:
                draw_snot = True

            if keys[pygame.K_ESCAPE]:
                print("\n Bye!")
                finished = True

            speak = ''
            for key, text in speech_from_key.items():
                if keys[key]:
                    speak = text
                    break
        else:
            speak = player_speak

        if len(tear_Ys) > 0:
            for i in range(len(tear_Ys)):
                tear_Ys[i] += 5
            if tear_Ys[0] > 480:
                tear_Ys.pop(0)

        screen.fill(pygame.Color('grey'))

        if len(eyelid_auto_values) > 0:
            # If the list of automated values isn't empty, we need to take
            # the next value off the list and use it to set the eyelids'
            # position.
            eyelids = eyelid_auto_values.pop(0)

        pygame.draw.rect(screen, pygame.Color('white'), (50, 50, 50, 50))
        pygame.draw.rect(screen, pygame.Color('white'), (700, 50, 50, 50))
        pygame.draw.rect(screen, pygame.Color('brown'), (700 + eyes, 50 + eyes_up, 10, 10))
        pygame.draw.rect(screen, pygame.Color('brown'), (50 + eyes, 50 + eyes_up, 10, 10))

        # Eyelids.  They're a bit wider than the eyeballs and start just
        # above them.  They close downwards, so their height is what
        # changes.
        pygame.draw.rect(screen, pygame.Color(150, 150, 175), (45, 45, 60, eyelids))
        pygame.draw.rect(screen, pygame.Color(150, 150, 175), (695, 45, 60, eyelids))

        total_space = 800 - mouth_wide
        mouth_space = total_space / 2

        pygame.draw.rect(screen, pygame.Color('pink'), (mouth_space, 450,
                                                        mouth_wide, 100 + mouth_height))

        if draw_snot:
            pygame.draw.circle(screen, pygame.Color('green'), (380, 400), 20)

        pygame.draw.rect(screen, pygame.Color(120, 120, 120), (350, 300, 100, 100))

        for tear_Y in tear_Ys:
            pygame.draw.circle(screen, pygame.Color(120, 120, 255), (100, tear_Y), 15)
            pygame.draw.circle(screen, pygame.Color(120, 120, 255), (700, tear_Y), 15)

        speech = myfont.render(speak, 1, (255, 0, 0))
        speech_width, speech_height = speech.get_size()
        speech_x = 400 - (speech_width / 2)
        screen.blit(speech, (speech_x, 535))

        pygame.display.flip()

game_thread = threading.Thread(target=game_loop)
game_thread.start()
game_thread.join()