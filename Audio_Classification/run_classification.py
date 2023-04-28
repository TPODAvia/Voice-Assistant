from tensorflow.keras.models import load_model
import tensorflow
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
import numpy as np
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

model = load_model(SCRIPT_DIR + '/models/lstm.h5',
custom_objects={'STFT':STFT,
                'Magnitude':Magnitude,
                'ApplyFilterbank':ApplyFilterbank,
                'MagnitudeToDecibel':MagnitudeToDecibel})

def make_prediction(sr, wav_fn):
   
    clean_wav=wav_fn
    step = sr
    batch = []

    for i in range(0, clean_wav.shape[0], step):
        sample = clean_wav[i:i+step]
        sample = sample.reshape(-1, 1)
        if sample.shape[0] < step:
            tmp = np.zeros(shape=(step, 1), dtype=np.float32)
            tmp[:sample.shape[0],:] = sample.flatten().reshape(-1, 1)
            sample = tmp
        batch.append(sample)
    X_batch = np.array(batch, dtype=np.float32)
    y_pred = model.predict(X_batch)
    y_mean = np.mean(y_pred, axis=0)

    return y_mean


if __name__ == '__main__':

    from clean import downsample_mono

    # parser = argparse.ArgumentParser(description='Audio Classification Training')
    # parser.add_argument('--sr', type=int, default=16000, help='sample rate of clean audio')
    # args, _ = parser.parse_known_args()

    wav_fn = SCRIPT_DIR + '/wavfiles/Snare_drum/ae7d1c37.wav'

    sr = 16000
    rate, clean_wav = downsample_mono(wav_fn, sr)
    result = make_prediction(sr, clean_wav)
    print("Answer: ", result)

