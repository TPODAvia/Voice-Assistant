from tensorflow.keras.models import load_model
from clean import downsample_mono
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
# from sklearn.preprocessing import LabelEncoder
import numpy as np
# from glob import glob
import argparse
import os
# import pandas as pd
# from tqdm import tqdm


def make_prediction(args, wav_fn):
    model = load_model(args.model_fn,
        custom_objects={'STFT':STFT,
                        'Magnitude':Magnitude,
                        'ApplyFilterbank':ApplyFilterbank,
                        'MagnitudeToDecibel':MagnitudeToDecibel})
    results = []
    rate, clean_wav = downsample_mono(wav_fn, args.sr)
    step = int(args.sr*args.dt)
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
    # y_pred = np.argmax(y_mean)
    # real_class = os.path.dirname(wav_fn).split('/')[-1]
    # print('Actual class: {}, accuracy {}'.format(real_class, y_mean[y_pred]))
    # results.append(y_mean)
    # np.save(os.path.join('logs', args.pred_fn), np.array(results))

    return y_mean


if __name__ == '__main__':

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

    wav_fn ='wavfiles/Snare_drum/ae7d1c37.wav'
    result = make_prediction(args, wav_fn)
    print("Answer: ", result)

