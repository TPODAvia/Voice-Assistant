import sys
import os
import numpy as np

sys.path.insert(0, "../")

from utilss import audio
from params.params import Params as hp


if __name__ == '__main__':
    import argparse
    import re
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--css10_directory",      type=str,   default="/home/vboxuser/Voice-Assistant/Multilingual_Text_to_Speech/data/css10",          help="Base directory of CSS10.")
    parser.add_argument("--css_comvoi_directory", type=str,   default="/home/vboxuser/Voice-Assistant/Multilingual_Text_to_Speech/data/css_comvoi/",    help="Base directory of Common Voice.")
    parser.add_argument("--comvoi_directory",     type=str,   default="/home/vboxuser/Voice-Assistant/Multilingual_Text_to_Speech/data/comvoi_clean/",  help="Base directory of prepared Voice")
    parser.add_argument("--sample_rate",          type=int,   default=22050, help="Sample rate.")
    parser.add_argument("--num_fft",              type=int,   default=1102,  help="Number of FFT frequencies.")
    parser.add_argument("--num_mels",             type=int,   default=80,    help="Number of mel bins.")
    parser.add_argument("--stft_window_ms",       type=float, default=50,    help="STFT window size.")
    parser.add_argument("--stft_shift_ms",        type=float, default=12.5,  help="STFT window shift.")
    parser.add_argument("--no_preemphasis",         action='store_false',    help="Do not use preemphasis.")
    parser.add_argument("--preemphasis",          type=float, default=0.97,  help="Strength of preemphasis.")

    args = parser.parse_args()

    hp.sample_rate = args.sample_rate
    hp.num_fft = args.num_fft

    files_to_solve = [
        (args.css10_directory, "train.txt"),
        (args.css10_directory, "val.txt"),
        (args.css_comvoi_directory, "train.txt"),
        (args.css_comvoi_directory, "val.txt"),
    ]

    spectrogram_dirs = [os.path.join(args.comvoi_directory, 'spectrograms'), 
                        os.path.join(args.comvoi_directory, 'linear_spectrograms')]
    
    for x in spectrogram_dirs:
        if not os.path.exists(x): os.makedirs(x)

    metadata = []
    for d, fs in files_to_solve:
        with open(os.path.join(d,fs), 'r', encoding='utf-8') as f:
            metadata.append((d, fs, [line.rstrip().split('|') for line in f]))

    print(f'Please wait, this may take a very long time.')
    for d, fs, m in metadata:  
        print(f'Creating spectrograms for: {fs}')

        with open(os.path.join(d, fs), 'w', encoding='utf-8') as f:
            for i in m:
                idx, s, l, a, _, _, raw_text, ph = i
                spec_name = idx + '.npy'      
                audio_path = os.path.join(d, a)  
                print("Path relate: ", d)     
                print("Audio data: ", a)   
                audio_data = audio.load(audio_path)

                splitted_a = a.split("/")
                if splitted_a[0] == "..":
                    mel_path_partial = os.path.join(splitted_a[0], splitted_a[1], spec_name)
                    lin_path_partial = os.path.join(splitted_a[0], splitted_a[1], spec_name)
                else:
                    mel_path_partial = spec_name
                    lin_path_partial = spec_name

                mel_path = os.path.join(spectrogram_dirs[0], mel_path_partial)
                if not os.path.exists(mel_path):
                    np.save(mel_path, audio.spectrogram(audio_data, True))
                lin_path = os.path.join(spectrogram_dirs[1], lin_path_partial)
                if not os.path.exists(lin_path):
                    np.save(lin_path, audio.spectrogram(audio_data, False))

                print(f'{idx}|{s}|{l}|{a}|{mel_path}|{lin_path}|{raw_text}|', file=f)