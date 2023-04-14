# TTS plugin for for emotional speech
# Author: TPODAvia

import os
import sys

from vacore import VACore
from vosk_tts.model import Model
from vosk_tts.synth import Synth


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
            "emotts": (init,say,None) # первая функция инициализации, вторая - говорить, третья - в wav file
                                         # если вторая - None, то используется 3-я с проигрыванием файла
        }
    }
    return manifest

def init(core:VACore):
    pass

def say(core:VACore, text_to_speech:str):

    import librosa
    import scipy
    sys.path.append("/home/vboxuser/Voice-Assistant/Multilingual_Text_to_Speech")
    from utilss import audio
    from params.params import Params as hp
    import numpy as np
    import torch

    checkpoint = "/home/vboxuser/Voice-Assistant/generated_switching.pyt"
    torch.load(checkpoint, map_location="cpu")['parameters']
    hp.decoder_language_init = False

    model = build_model(checkpoint)
    model.eval()

    inputs = []
    for s, l in [("09-ru","ru")]:
        inputs += [
            f"Совет обладает полномочиями по руководству всей операционной деятельностью Центрального банка и контролю за коммерческими оманскими банками.|{s}|{l}",
        ]

    generated_spectrograms = inference(model, inputs, "cpu")

    for i, s in enumerate(generated_spectrograms):
        s = audio.denormalize_spectrogram(s, not hp.predict_linear)
        w = audio.inverse_spectrogram(s, not hp.predict_linear)
        print(w, w.shape)

        # write output
        scipy.io.wavfile.write('test.wav', hp.sample_rate, np.array(w*4, dtype=np.float32))

def towavfile(core:VACore, text_to_speech:str,wavfile:str):
    pass

def build_model(checkpoint):
    
    import torch
    from params.params import Params as hp
    from utilss import remove_dataparallel_prefix
    # from utilss.logging import Logger
    from modules.tacotron2 import Tacotron

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    state = torch.load(checkpoint, map_location=device)
    hp.load_state_dict(state['parameters'])

    model = Tacotron()
    model_dict = model.state_dict()
    pretrained_dict = remove_dataparallel_prefix(state['model'])
    
    missing = [k for k, _ in pretrained_dict.items() if k not in model_dict]
    print(f'Missing model parts: {missing}')
    
    missing = [k for k, _ in model_dict.items() if k not in pretrained_dict]
    print(f'Extra model parts: {missing}')
    
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
    
    model_dict.update(pretrained_dict) 
    model.load_state_dict(model_dict) 
    model.to(device)
    
    return model

def inference(model, inputs, device=None):

    import torch
    from params.params import Params as hp
    from utilss import text

    inputs = [l.rstrip().split('|') for l in inputs if l]

    spectrograms = []
    for i in inputs:
        
        clean_text = i[0]

        if not hp.use_punctuation: 
            clean_text = text.remove_punctuation(clean_text)
        if not hp.case_sensitive: 
            clean_text = text.to_lower(clean_text)
        if hp.remove_multiple_wspaces: 
            clean_text = text.remove_odd_whitespaces(clean_text)
        
        t = torch.LongTensor(text.to_sequence(clean_text, use_phonemes=hp.use_phonemes))
        
        if hp.multi_language:     
            l_tokens = i[2].split(',')
            t_length = len(clean_text) + 1
            l = []
            for token in l_tokens:
                l_d = token.split('-')
 
                language = [0] * hp.language_number
                for l_cw in l_d[0].split(':'):
                    l_cw_s = l_cw.split('*')
                    language[hp.languages.index(l_cw_s[0])] = 1 if len(l_cw_s) == 1 else float(l_cw_s[1])
                language_length = (int(l_d[1]) if len(l_d) == 2 else t_length)
                l += [language] * language_length
                t_length -= language_length     
            l = torch.FloatTensor([l])
        else:
            l = None

        s = torch.LongTensor([hp.unique_speakers.index(i[1])]) if hp.multi_speaker else None

        if device=="cuda" or (device is None and torch.cuda.is_available()): 
            t = t.cuda(non_blocking=True)
            if l: l = l.cuda(non_blocking=True)
            if s: s = s.cuda(non_blocking=True)
     
        spectrograms.append(model.inference(t, speaker=s, language=l).cpu().detach().numpy())

    return spectrograms