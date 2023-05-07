import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import sys
import os
import random
import time
from numpy import save, argmax, dot
from numpy.linalg import norm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Face_ui.img_library import library, img_library

class ImageLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.frames = []
        self.frame_rates = []
        self.loc = 0

    def load(self, text_input):
        self.config(image="")
        self.frames.clear()
        self.frame_rates.clear()

        folder_path = self.pred(text_input)
        gif_file = self.select_random_gif(folder_path)

        self.load_frames_and_rates(gif_file)

        if self.frames:
            self.config(image=self.frames[0])
            self.next_frame(self.loc)

    def select_random_gif(self, folder_path):
        gif_files = [f for f in os.listdir(folder_path) if f.endswith('.gif')]
        random_gif = random.choice(gif_files)
        return os.path.join(folder_path, random_gif)

    def load_frames_and_rates(self, gif_file):
        with Image.open(gif_file) as im:
            for frame in ImageSequence.Iterator(im):
                frame_duration = frame.info['duration']
                frame_rate = frame_duration if frame_duration > 0 else 0
                self.frame_rates.append(frame_rate)
                
                # Resize the frame to 50% of its original size
                new_width = int(frame.width * 0.5)
                new_height = int(frame.height * 0.5)
                resized_frame = frame.resize((new_width, new_height))

                self.frames.append(ImageTk.PhotoImage(resized_frame.copy()))

    def unload(self):
        self.config(image="")
        self.frames.clear()

    def next_frame(self, loc):
        global run_prediction

        if run_prediction:
            global text_input
            run_prediction = False
            self.load(text_input)

        if self.frames:
            loc += 1
            loc %= len(self.frames)
            self.config(image=self.frames[loc])
            self.after(self.frame_rates[loc], self.next_frame, loc)

    def pred(self, text_input):
        
        list = []
        for i in range(len(library)):
            # counting cosine similarity
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

        image_path = SCRIPT_DIR + '/face expression/' + img_library[pred]

        return image_path

def close_win(event):
    lbl.unload()
    root.destroy()
    global my_event
    my_event = False

def run_tkinter():
    global root
    root = tk.Tk()
    root.bind('<Escape>', close_win)
    global lbl
    lbl = ImageLabel(root)
    lbl.pack()
    global text_input
    lbl.load(text_input)
    root.mainloop()


if __name__ == '__main__':
    
    # Run the tkinter event loop in a separate thread
    tkinter_thread = threading.Thread(target=run_tkinter)
    tkinter_thread.start()
    my_event = True

    # Global variable input
    text_input = [  0,2,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ]
    run_prediction = False
    time.sleep(5)

    while my_event:
        # Your other code goes here
        print("Executing other code...")
        time.sleep(1)

        text_input = [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ]
        run_prediction = True
        time.sleep(10)

        text_input = [  0,1,0,0, 1,0,0,0, 0,0,0,0, 0,1,0,0, 0,0,0,0, 0,1,0,0, 0,1  ]
        run_prediction = True
        time.sleep(10)

        text_input = [  0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ]
        run_prediction = True
        time.sleep(10)