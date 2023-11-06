# if you have problems with PyAudio install, check this:
# https://github.com/EnjiRouz/Voice-Assistant-App/blob/master/README.md

import time
start_time = time.time()
import numpy as np
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
current_path = os.getcwd()
if current_path != SCRIPT_DIR:
    print("\n\n")
    print("#"*100)
    sys.exit('Program can only be run from path ' + SCRIPT_DIR)
import whisper
import re
import threading
import argparse
import pyaudio
from openwakeword.model import Model
import speech_recognition
from vacore import VACore

# sys.path.apspend(os.path.dirname(SCRIPT_DIR) + "/Audio_Classification")
# import run_classification
# sys.path.append(os.path.dirname(SCRIPT_DIR) + "/Face_ui")
# import run_gif

# Load the Whisper model
whisper.load_model("base")

# Duration in seconds for the timer
_timer_duration = 30
_recognized_data = ""
_interrupted = True

class WorkerThread(threading.Thread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.stop = False
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

        with self.microphone:
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=1)

    def run(self):

        global _interrupted
        while _interrupted and not self.stop:
            with self.microphone:
                global _recognized_data
                with speech_recognition.Microphone(sample_rate=16000) as source:                
                    print("Listening...")
                    audio = self.recognizer.listen(source)
                    # audio_data = audio.get_wav_data()
                    # data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
                    # float_data = data_s16.astype(np.float32, order='C') / 32768.0
                try:
                    print("Started recognition...")
                    _recognized_data = self.recognizer.recognize_whisper(audio, model="base", language="russian")

                except speech_recognition.UnknownValueError:
                    pass

                # в случае проблем с доступом в Интернет происходит выброс ошибки
                except speech_recognition.RequestError:
                    print("Check your Internet Connection, please")
                return _recognized_data #, emo_classf

# Parse input arguments
parser=argparse.ArgumentParser()
parser.add_argument(
    "--chunk_size", help="How much audio (in number of samples) to predict on at once",
    type=int, default=1280, required=False
)
parser.add_argument(
    "--model_path", help="The path of a specific model to load",
    type=str, default="", required=False
)
parser.add_argument(
    "--inference_framework",
    help="The inference framework to use (either 'onnx' or 'tflite'",
    type=str, default='tflite', required=False
)
args=parser.parse_args()


def my_function():

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = args.chunk_size
    audio = pyaudio.PyAudio()
    mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Load pre-trained openwakeword models
    if args.model_path != "":
        owwModel = Model(wakeword_models=[args.model_path], inference_framework=args.inference_framework)
    else:
        owwModel = Model(inference_framework=args.inference_framework)

    threads = []
    count = 0
    thread_activate = True
    waiting_activate = False
    global _interrupted
    global start_time
    global _timer_duration
    while _interrupted:

        # print("Second thread doing some work...")
        audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
        owwModel.predict(audio)

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
                        start_time = time.time()  # Store the current time as the start time
                        thread = WorkerThread()
                        thread.start()
                        time.sleep(0.4)
                        threads.append(thread)

            elif mdl == "5_minute_timer":
                scores = list(owwModel.prediction_buffer[mdl])
                if scores[-1] <= 0.5:
                    pass
                else:
                    print("Okay, the timer have started")

        # The feature is not working. Requres to add speaking excecution detection.
        # print(threads)
        # elapsed_time = time.time() - start_time
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

    core = VACore()
    core.init_with_plugins()

    my_thread = threading.Thread(target = my_function)
    my_thread.start()

    try:
        while _interrupted:

            # print("_recognized_data: " + str(_recognized_data))
            # print(_recognized_data)
            voice_input_str = _recognized_data
            time.sleep(1)

            # remove punctuations and caps: Ирина, привет! --> ирина привет
            no_punct_str = re.sub(r'[^\w\s]', '', voice_input_str)
            lowercase_str = no_punct_str.lower().strip()

            # print(lowercase_str)

            if (lowercase_str != "" 
                and lowercase_str != "редактор субтитров асемкин корректор аегорова" 
                and lowercase_str != "субтитры и редактор субтитров асемкин корректор всухиашвили"):

                # Check if the timer has reached its duration
                elapsed_time = time.time() - start_time
                if elapsed_time >= _timer_duration:

                    print("First statement is active")
                    haveRun = core.run_input_str("ирина " + lowercase_str)
                    
                    if haveRun:
                        start_time = time.time()  # Store the current time as the start time

                else: # second_statement_active:
                    print("Second statement is active")

                    start_time = time.time()
                    core.context_set(lowercase_str)
                    core.run_input_str(lowercase_str)

                _recognized_data = ""
            core._update_timers()
    except KeyboardInterrupt:
        _interrupted = False