# you need to install:
# pip install PyAudio
# pip install SpeechRecognition

# if you have problems with PyAudio install, check this:
# https://github.com/EnjiRouz/Voice-Assistant-App/blob/master/README.md

import speech_recognition
import traceback
from vacore import VACore
from threading import Thread
import pyaudio
import wave
import numpy as np

import argparse
import sys
sys.path.append("/home/vboxuser/Voice-Assistant/")
# from Audio_Classification import run_classification
# from ReactionGIF import run_reaction
from Face_ui import run_face

# most from @EnjiRouz code: https://habr.com/ru/post/529590/
def task():

    pass

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('done saving')



    parser = argparse.ArgumentParser(description='Audio Classification Training')
    parser.add_argument('--model_fn', type=str, default='models/lstm.h5',
                        help='model file to make predictions')
    parser.add_argument('--pred_fn', type=str, default='y_pred',
                        help='fn to write predictions in logs dir')
    parser.add_argument('--src_dir', type=str, default='wavfiles',
                        help='directory containing wavfiles to predict')
    parser.add_argument('--dt', type=float, default=1.0,
                        help='time in seconds to sample audio')
    parser.add_argument('--sr', type=int, default=16000,
                        help='sample rate of clean audio')
    parser.add_argument('--threshold', type=str, default=20,
                        help='threshold magnitude for np.int16 dtype')
    args, _ = parser.parse_known_args()

    wav_fn ='/home/vboxuser/Voice-Assistant/Audio_Classification/wavfiles/Acoustic_guitar/0eeaebcb.wav'
    emo_classf = run_classification.make_prediction(args, wav_fn )

    # print(emo_classf)

    return emo_classf


def def_persona():
    
    pass




def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        try:
            #print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        try:
            #print("Started recognition...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            print("Check your Internet Connection, please")

        return recognized_data


if __name__ == "__main__":
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


    while True:
        # старт записи речи с последующим выводом распознанной речи
        print("Hello1")
        # t2 = Thread(emo_classf=task)
        # t2.start()
        voice_input_str = record_and_recognize_audio()
        # t2.join()
        
        print("Hello2: ")
        t2 =   [1,0,0,0, 1,1,0,0, 0,0,1,0, 0,1,0,1, 0,0,0,0, 0,1,0,0, 0,1]

        
        the_reaction = [1,0,0,0, 1,1,0,0, 0,0,1,0, 0,1,0,1, 0,0,0,0, 0,1,0,0, 0,1] # run_reaction.reaction(voice_input_str)
        
        combined_reaction = np.maximum(t2, the_reaction)

        run_face.main(combined_reaction)

        if voice_input_str != "":
            core.run_input_str(voice_input_str)

        print("Hello3")
        core._update_timers()

        print("Hello4")