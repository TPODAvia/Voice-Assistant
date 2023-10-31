# TTS plugin for for emotional speech
# Author: TPODAvia

import os
import sys
import glob
import random

from vacore import VACore
import torch
import phonemizer
from numpy import load
from playsound import playsound

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get all WAV files in the folder
wav_files = glob.glob(os.path.dirname(os.path.dirname(SCRIPT_DIR)) + "/Voices/humble/*.wav")

sys.path.append(os.path.dirname(os.path.dirname(SCRIPT_DIR)) + "/StyleTTS/Demo")
from run_tts import from_pretrained, main, save_wave_scipy

# load phonemizer
global_phonemizer = phonemizer.backend.EspeakBackend(language='ru', preserve_punctuation=True,  with_stress=True)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model, generator, textclenaer = from_pretrained(device)

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "TTS emotion",
        "version": "1.1",
        "require_online": False,

        # "default_options": {
        #     "sysId": 0, # id голоса в системе, может варьироваться
        # },

        "tts": {
            "emotts": (init,None,towavfile) # первая функция инициализации, вторая - говорить, третья - в wav file
                                         # если вторая - None, то используется 3-я с проигрыванием файла
        }
    }
    return manifest

def init(core:VACore):
    pass

def say(core:VACore, text_to_speech:str):

    pass

def towavfile(core:VACore, text_to_speech:str,wavfile:str):

    # run if text input is long
    if len(text_to_speech) > 30:
        random_wav = random.choice(wav_files)
        playsound(random_wav, False)


    n = load(os.path.dirname(SCRIPT_DIR) + "/tts_cache/emotts/emotion.npy")

    emotion = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']

    ref_dicts = {}
    ref_dicts[emotion[n]] = "Some comments" # the output is:{"Emotion":"Some comments" }

    save_wave_scipy(wavfile, main(text_to_speech, ref_dicts, model, generator, textclenaer, device, global_phonemizer), 24000)

    pass