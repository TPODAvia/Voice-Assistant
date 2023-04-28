# you need to install:
# pip install PyAudio
# pip install SpeechRecognition

# if you have problems with PyAudio install, check this:
# https://github.com/EnjiRouz/Voice-Assistant-App/blob/master/README.md

import speech_recognition
from vacore import VACore
import asyncio
import sounddevice as sd
import numpy as np
import cv2
import argparse
import os
import sys
import whisper
import re
from simpletransformers.classification import MultiLabelClassificationModel

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(SCRIPT_DIR) + "/Audio_Classification")
import run_classification

sys.path.append(os.path.dirname(SCRIPT_DIR) + "/Face_ui")
import run_face

# Load the Whisper model
whisper_model = whisper.load_model("base")

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
            #print("Started recognition...")
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

    if voice_input_str != "":
        core.run_input_str(lowercase_str)


    core._update_timers()

    return voice_input_str, emo_classf


async def function3(result): # function3(result1, result2)

    if not result[0]=="":
        predictions, raw_outputs = model.predict([result[0]])
        combined_reaction = np.maximum(result[1], raw_outputs)

    else:
        combined_reaction = result[1]

        
    img = run_face.main(combined_reaction)
    cv2.imshow('Hello', img)
    cv2.waitKey(1)


async def main():

    while True:
        # results = await asyncio.gather(function_2(), function_async())
        results = await asyncio.gather(function_2())
        await function3(*results)

if __name__ == "__main__":

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
