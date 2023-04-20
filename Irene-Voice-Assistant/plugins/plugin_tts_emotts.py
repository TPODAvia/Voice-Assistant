# TTS plugin for for emotional speech
# Author: TPODAvia

import os
import sys

from vacore import VACore

from tqdm import tqdm
import torch

sys.path.append("/home/vboxuser/Voice-Assistant/Multilingual_Text_to_Speech")
from utilss import audio, text
from utilss import build_model
from params.params import Params as hp

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

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default="/home/vboxuser/Voice-Assistant/Multilingual_Text_to_Speech/checkpoints/generated_switching.pyt", help="Model checkpoint.")
    parser.add_argument("--output", type=str, default=".", help="Path to output directory.")
    parser.add_argument("--seed", type=int, default=None, help="Torch random seed.")
    parser.add_argument("--cpu", action='store_true', help="Force to run on CPU.")
    parser.add_argument("--save_spec", action='store_true', help="Saves also spectrograms if set.")
    parser.add_argument("--ignore_wav", action='store_true', help="Does not save waveforms if set.")
    args = parser.parse_args()

    if args.seed is not None:
        print(f"Random seed set to {args.seed}")
        torch.manual_seed(args.seed)

    print("Building model ...")

    model = build_model(args.checkpoint, args.cpu)
    model.eval()

    #total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    #print(f"Builded model with {total_params} parameters")

    inputs = ["04|" + text_to_speech + "|00-de|ru"]
    progress = tqdm(enumerate(inputs), total=len(inputs), desc='Synthesizing')

    spectrograms = []
    for i, item in progress:
        progress.set_postfix_str(item)

        item_id = item.split("|")[0]
        if item_id == "":
            item_id = i

        s = synthesize(model, item, args.cpu)

        if not os.path.exists(args.output):
            os.makedirs(args.output)

        # if args.save_spec:
        #     np.save(os.path.join(args.output, f'{item_id}.npy'), s)

        if not args.ignore_wav:
            w = audio.inverse_spectrogram(s, not hp.predict_linear)
            audio.save(w, os.path.join(args.output, f'temp/vacore_1.wav'))

    pass

def synthesize(model, input_data, force_cpu=False):

    item = input_data.split('|')
    clean_text = item[1]

    if not hp.use_punctuation: 
        clean_text = text.remove_punctuation(clean_text)
    if not hp.case_sensitive: 
        clean_text = text.to_lower(clean_text)
    if hp.remove_multiple_wspaces: 
        clean_text = text.remove_odd_whitespaces(clean_text)

    t = torch.LongTensor(text.to_sequence(clean_text, use_phonemes=hp.use_phonemes))

    if hp.multi_language:     
        l_tokens = item[3].split(',')
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

    s = torch.LongTensor([hp.unique_speakers.index(item[2])]) if hp.multi_speaker else None

    if torch.cuda.is_available() and not force_cpu: 
        t = t.cuda(non_blocking=True)
        if l is not None: l = l.cuda(non_blocking=True)
        if s is not None: s = s.cuda(non_blocking=True)

    s = model.inference(t, speaker=s, language=l).cpu().detach().numpy()
    s = audio.denormalize_spectrogram(s, not hp.predict_linear)

    return s