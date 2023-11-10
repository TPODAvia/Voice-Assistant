import time
_start_time = time.time()
import numpy as np
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
current_path = os.getcwd()
if current_path.upper() != SCRIPT_DIR.upper():
    print("\n\n")
    print("#"*100)
    print("Current path: " + str(current_path))
    sys.exit('Program can only be run from path ' + SCRIPT_DIR + "\n")

import whisper
import re
import threading
import argparse
import pyaudio
from openwakeword.model import Model
import speech_recognition
import signal
from vacore import VACore

sys.path.append(os.path.dirname(SCRIPT_DIR))
import AudioReaction.engine
import Face_ui.run_gif

# Load the Whisper model
whisper.load_model("base")

# Duration in seconds for the timer
_timer_duration = 30
# the NN service is opened as a default. Turn this off to fully run offline.
VACore.using_internet_service = True
# other variables to properly run the program
_recognized_data = ""
_runva_looping = True
Face_ui.run_gif._gif_looping = True
Face_ui.run_gif._text_input = [  0,2,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ] #26
Face_ui.run_gif._run_prediction = False

# Parse input arguments
parser=argparse.ArgumentParser()

parser.add_argument("--model_path", type=str, default="", required=False, 
                    help="The path of a specific model to load")
parser.add_argument('--model_class_file', type=str, default="D:\Coding_AI\Voice-Assistant\AudioReaction\wakeword_m.pt", required=False,
                    help='optimized file to load. use optimize_graph.py')
args=parser.parse_args()

class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.stop = False
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

        with self.microphone:
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=0.3)

    def run(self):

        global _runva_looping
        while _runva_looping and not self.stop:
            with self.microphone:
                global _recognized_data
                with speech_recognition.Microphone(sample_rate=16000) as source:                
                    print("Listening...")
                    audio = self.recognizer.listen(source)
                    # audio_data = audio.get_wav_data()
                    # data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
                    # float_data = data_s16.astype(np.float32, order='C') / 32768.0
                try:

                    if VACore.available_internet == True:
                        _recognized_data = self.recognizer.recognize_google(audio, language="ru").lower()
                    else:
                        print("Started recognition...")
                        _recognized_data = self.recognizer.recognize_whisper(audio, model="base", language="russian")

                except speech_recognition.UnknownValueError:
                    pass

                # в случае проблем с доступом в Интернет происходит выброс ошибки
                except speech_recognition.RequestError:
                    print("Check your Internet Connection, please")
                return _recognized_data #, emo_classf

def neural_function():

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 8000
    FRAMEWORK = "tflite" # onx or tflite
    audio = pyaudio.PyAudio()
    mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Load pre-trained openwakeword models
    if args.model_path != "":
        owwModel = Model(wakeword_models=[args.model_path], inference_framework=FRAMEWORK)
    else:
        owwModel = Model(inference_framework=FRAMEWORK)

    arModel = AudioReaction.engine.ClassificationEngine(model_class_file=args.model_class_file)

    threads = []
    count = 0
    thread_activate = True
    waiting_activate = False
    global _runva_looping
    global _start_time
    global _timer_duration
    tensor_normalized_output = []

    tkinter_thread = threading.Thread(target=Face_ui.run_gif.run_tkinter)
    tkinter_thread.start()

    while _runva_looping:

        # print("Second thread doing some work...")
        audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
        owwModel.predict(audio)

        tensor_normalized_output = arModel.predict(audio)

        count += 1
        if count > 100:
            count = 0

            if not tensor_normalized_output == []:
                # this convert from tensor([[-0.05634324  0.47326437  0.8782495   0.03904041]])
                # to [[-0.05634324  0.47326437  0.8782495   0.03904041]] using .numpy
                # finaly [-0.05634324  0.47326437  0.8782495   0.03904041] using .flatten()
                output = tensor_normalized_output.numpy().flatten()
                print(len(output))
                if len(output) == 26:
                    # _text_input requres arrays of 26: [1, 2, 3 ... 26]
                    Face_ui.run_gif._text_input = output
                    Face_ui.run_gif._run_prediction = True

        for mdl in owwModel.prediction_buffer.keys():

            if mdl == "alexa":
                scores = list(owwModel.prediction_buffer[mdl])

                if scores[-1] <= 0.5:
                    thread_activate = True
                else:
                    if thread_activate:
                        print("Hearing...")
                        thread_activate = False
                        waiting_activate = False
                        _start_time = time.time()  # Store the current time as the start time
                        thread = WorkerThread()
                        thread.start()
                        threads.append(thread)
                        time.sleep(0.4)
                        
            elif mdl == "5_minute_timer":
                scores = list(owwModel.prediction_buffer[mdl])
                if scores[-1] <= 0.5:
                    pass
                else:
                    print("Okay, the timer have started")

        # The feature is not working. Requres to add speaking excecution detection.
        # print(threads)
        # elapsed_time = time.time() - _start_time
        # if elapsed_time <= 10:
        #     if not threads and waiting_activate:
        #         # print("thread_activate")
        #         # print(threads)
        #         thread = WorkerThread()
        #         thread.start()
        #         time.sleep(0.2)
        #         threads.append(thread)
        
        # if elapsed_time > 4:
        #     waiting_activate = True

        # deleting the 
        threads_alive = []
        for t in threads:
            if not t.is_alive():
                t.join()
            else:
                threads_alive.append(t)

        threads = threads_alive

        # Stop the threads after a certain time
        for thread in threads:
            thread.stop = True

if __name__ == "__main__":

    def signal_handler(signal, frame):
        print("Ctrl+C pressed. Stopping threads...")
        global _runva_looping
        _runva_looping = False
        Face_ui.run_gif._gif_looping = False

    core = VACore()
    core.init_with_plugins()

    signal.signal(signal.SIGINT, signal_handler)
    neural_thread = threading.Thread(target = neural_function)
    neural_thread.start()

    try:
        while _runva_looping:

            # print("_recognized_data: " + str(_recognized_data))
            # print(_recognized_data)
            voice_input_str = _recognized_data

            if VACore.is_internet_available() and VACore.using_internet_service:
                VACore.available_internet = True
            else:
                VACore.available_internet = False

            # remove punctuations and caps: Ирина, привет! --> ирина привет
            no_punct_str = re.sub(r'[^\w\s]', '', voice_input_str)
            lowercase_str = no_punct_str.lower().strip()

            # print(lowercase_str)

            if (lowercase_str != "" 
                and lowercase_str != "редактор субтитров асемкин корректор аегорова" 
                and lowercase_str != "субтитры и редактор субтитров асемкин корректор всухиашвили"):

                # Check if the timer has reached its duration
                elapsed_time = time.time() - _start_time
                if elapsed_time >= _timer_duration:

                    print("First statement is active")
                    haveRun = core.run_input_str("ирина " + lowercase_str)
                    
                    if haveRun:
                        _start_time = time.time()  # Store the current time as the start time

                else: # second_statement_active:
                    print("Second statement is active")

                    _start_time = time.time()
                    core.context_set(lowercase_str)
                    core.run_input_str(lowercase_str)

                _recognized_data = ""
            core._update_timers()
    except KeyboardInterrupt:
        _runva_looping = False