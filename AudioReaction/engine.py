"""the interface to interact with wakeword model"""
import pyaudio
import threading
import time
import argparse
import wave
import torchaudio
import torch
import numpy as np
from neuralnet.dataset import index_to_label, get_likely_index
from threading import Event


class Listener:

    def __init__(self, sample_rate=8000, record_seconds=2):
        self.chunk = 1024
        self.sample_rate = sample_rate
        self.record_seconds = record_seconds
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=self.chunk)

    def listen(self, queue):
        while True:
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("\nWake Word Engine is now listening... \n")


class WakeWordEngine:

    def __init__(self, model_file):
        self.listener = Listener(sample_rate=8000, record_seconds=2)
        self.model = torch.jit.load(model_file)
        self.model.eval().to('cpu')  #run on cpu
        self.audio_q = list()

    def save(self, waveforms, fname="wakeword_temp"):
        wf = wave.open(fname, "wb")
        # set the channels
        wf.setnchannels(1)
        # set the sample format
        wf.setsampwidth(self.listener.p.get_sample_size(pyaudio.paInt16))
        # set the sample rate
        wf.setframerate(8000)
        # write the frames as bytes
        wf.writeframes(b"".join(waveforms))
        # close the file
        wf.close()
        return fname


    def predict(self, audio):
        with torch.no_grad():
            fname = self.save(audio)
            waveform, _ = torchaudio.load(fname)  # don't normalize on train

            # waveform, sample_rate, utterance, *_ = train_set[2]
            # print(len(waveform))
            # print(sample_rate)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            # transform = transform.to(device)
            tensor = waveform.to(device)
            # tensor = transform(tensor)
            print(tensor.shape)
            tensor = self.model(tensor.unsqueeze(0))
            tensor = get_likely_index(tensor)
            output = index_to_label(tensor.squeeze())
            return output

    def inference_loop(self, action):
        while True:
            if len(self.audio_q) > 15:  # remove part of stream
                diff = len(self.audio_q) - 15
                for _ in range(diff):
                    self.audio_q.pop(0)
                action(self.predict(self.audio_q))
            elif len(self.audio_q) == 15:
                action(self.predict(self.audio_q))
            time.sleep(0.05)

    def run(self, action):
        self.listener.run(self.audio_q)
        thread = threading.Thread(target=self.inference_loop,
                                    args=(action,), daemon=True)
        thread.start()


class DemoAction:
    """This demo action will just randomly say Arnold Schwarzenegger quotes

        args: sensitivty. the lower the number the more sensitive the
        wakeword is to activation.
    """
    def __init__(self, sensitivity=10):
        # import stuff here to prevent engine.py from 
        # importing unecessary modules during production usage
        import os
        import subprocess
        import random
        from os.path import join, realpath

        self.random = random
        self.subprocess = subprocess
        self.detect_in_row = 0

        self.sensitivity = sensitivity
        folder = realpath(join(os.path.dirname(os.path.abspath(__file__)), 'fun', 'arnold_audio'))
        self.arnold_mp3 = [
            os.path.join(folder, x)
            for x in os.listdir(folder)
            if ".wav" in x
        ]

    def __call__(self, prediction):
        if prediction == 1:   # change this to the class label you're interested in
            self.detect_in_row += 1
            if self.detect_in_row == self.sensitivity:
                self.play()
                self.detect_in_row = 0
        else:
            self.detect_in_row = 0

    def play(self):
        filename = self.random.choice(self.arnold_mp3)
        try:
            print("playing", filename)
            self.subprocess.check_output(['play', '-v', '.1', filename , '-t', 'alsa'])
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="demoing the wakeword engine")
    parser.add_argument('--model_file', type=str, default="D:\Coding_AI\Voice-Assistant\AudioReaction\wakeword_m.pt", required=False,
                        help='optimized file to load. use optimize_graph.py')
    parser.add_argument('--sensitivty', type=int, default=10, required=False,
                        help='lower value is more sensitive to activations')

    args = parser.parse_args()
    wakeword_engine = WakeWordEngine(args.model_file)
    action = DemoAction(sensitivity=60)

    print("""\n*** Make sure you have sox installed on your system for the demo to work!!!
    If you don't want to use sox, change the play function in the DemoAction class
    in engine.py module to something that works with your system.\n
    """)
    # action = lambda x: print(x)
    wakeword_engine.run(action)

    threading.Event().wait()
