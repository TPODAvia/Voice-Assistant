# you need to install:
# pip install PyAudio
# pip install SpeechRecognition

# if you have problems with PyAudio install, check this:
# https://github.com/EnjiRouz/Voice-Assistant-App/blob/master/README.md

import time
start_time = time.time()

import speech_recognition
from vacore import VACore
import asyncio
import numpy as np
import os
import sys
import whisper
import re
from simpletransformers.classification import MultiLabelClassificationModel
import threading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(SCRIPT_DIR) + "/Audio_Classification")
import run_classification

sys.path.append(os.path.dirname(SCRIPT_DIR) + "/Face_ui")
import run_gif

# Load the Whisper model
# whisper_model = whisper.load_model("base")


# Initialize variables
first_statement_active = True
timer_duration = 20  # Duration in seconds for the timer

# most from @EnjiRouz code: https://habr.com/ru/post/529590/

async def function_async():
    return None

def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        with speech_recognition.Microphone(sample_rate=16000) as source:
            print("Listening...")
            audio = recognizer.listen(source)
            audio_data = audio.get_wav_data()
            data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
            float_data = data_s16.astype(np.float32, order='C') / 32768.0
        try:
            print("Started recognition...")
            recognized_data = recognizer.recognize_whisper(audio, model="base", language="russian")

            sr=16000
            emo_classf = run_classification.make_prediction(sr, float_data)


        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")
        return recognized_data, emo_classf
    
async def function_2():

    voice_input_str, emo_classf = record_and_recognize_audio()

    # remove punctuations and caps: Ирина, привет! --> ирина привет
    no_punct_str = re.sub(r'[^\w\s]', '', voice_input_str)
    lowercase_str = no_punct_str.lower().strip()

    # print("recognized_data:", lowercase_str)
    global first_statement_active
    global start_time
    print("Sound:", lowercase_str)

    if lowercase_str != ("" or "редактор субтитров асемкин корректор аегорова"):

        # Check if the timer has reached its duration
        elapsed_time = time.time() - start_time
        if elapsed_time >= timer_duration:

            print("First statement is active")
            haveRun = core.run_input_str(lowercase_str)
            
            if haveRun:
                start_time = time.time()  # Store the current time as the start time

        else: # second_statement_active:
            print("Second statement is active")

            start_time = time.time()
            core.context_set(lowercase_str)
            core.run_input_str(lowercase_str)

    core._update_timers()

    return voice_input_str, emo_classf


async def function3(result): # function3(result1, result2)

    if not result[0]=="":
        predictions, raw_outputs = model.predict([result[0]])
        combined_reaction = np.maximum(result[1], raw_outputs)

    else:
        combined_reaction = result[1]

    global text_input
    global run_prediction
    text_input = combined_reaction
    run_prediction = True


async def main():

    # tkinter_thread = threading.Thread(target=run_gif.run_tkinter)
    # tkinter_thread.start()

    while True:
        # results = await asyncio.gather(function_2(), function_async())
        results = await asyncio.gather(function_2())
        await function3(*results)

if __name__ == "__main__":

    # Global variable input
    text_input = [  0,2,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ]
    run_prediction = False

    model = MultiLabelClassificationModel("roberta", os.path.dirname(SCRIPT_DIR) + "/ReactionGIF/outputs/checkpoint-9-epoch-3/", num_labels=26, use_cuda=False)

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    with microphone:
        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

    # initing core
    core = VACore()
    #core.init_plugin("core")
    #core.init_plugins(["core"])
    core.init_with_plugins()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
