"""the interface to interact with LSTM_10 model"""
import os
import sys
import pyaudio
import threading
import time
import argparse
import wave
import torchaudio
import torch
import signal
import numpy as np

_classification_loop = True

# Check if the current thread is the main thread
# if threading.current_thread() is threading.main_thread():
if __name__ == "__main__":
    # import stuff here to prevent engine.py from importing unecessary modules during production usage
    import subprocess
    import random
    from os.path import join, realpath

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    import Face_ui.run_gif

    Face_ui.run_gif._gif_looping = True
    Face_ui.run_gif._text_input = [  0,2,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ] #26
    Face_ui.run_gif._run_prediction = False

class Listener:

    def __init__(self, sample_rate=8000, record_seconds=1):
        self.chunk = 800
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
        global _classification_loop
        while _classification_loop:
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("\nWake Word Engine is now listening... \n")

class ClassificationEngine:

    def __init__(self, model_class_file):
        self.model = torch.jit.load(model_class_file)
        self.model.eval().to('cpu')  #run on cpu
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def predict(self, audio):
        with torch.no_grad():
            if str(type(audio)) == "<class 'str'>":
                waveform, sample_rate = torchaudio.load(audio)  # don't normalize on train
            else:
                audio = np.array(audio)
                buffer = audio.astype(np.float32) / 32767.0
                waveform_tensor = torch.from_numpy(buffer)
                waveform = waveform_tensor.unsqueeze(0)

            tensor = waveform.to(self.device)
            model_output = self.model(tensor.unsqueeze(0))

            # this normalized all numbers to [0...1]
            tensor_normalized_output = torch.nn.functional.normalize(model_output, p=2, dim=-1)

            return tensor_normalized_output

class DemoAction:
    """This demo action will just randomly say Arnold Schwarzenegger quotes
    """
    def __init__(self):
        self.random = random
        self.subprocess = subprocess
        self.detect_in_row = 0

        folder = realpath(join(os.path.dirname(os.path.abspath(__file__)), 'fun', 'arnold_audio'))
        self.arnold_mp3 = [
            os.path.join(folder, x)
            for x in os.listdir(folder)
            if ".wav" in x
        ]

    def play(self):
        filename = self.random.choice(self.arnold_mp3)
        try:
            print("playing", filename)
            self.subprocess.check_output(['play', '-v', '.1', filename , '-t', 'alsa'])
        except Exception as e:
            print(str(e))

    def save(self, waveforms, get_sample_size, fname="wakeword_temp"):
        wf = wave.open(fname, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(get_sample_size)
        wf.setframerate(8000)
        # write the frames as bytes
        wf.writeframes(b"".join(waveforms))
        wf.close()
        return fname

def classification_function():

    audio_q = list()
    listener = Listener(sample_rate=8000, record_seconds=1)
    get_sample_size = listener.p.get_sample_size(pyaudio.paInt16)
    classificator  = ClassificationEngine(args.model_class_file)
    action = DemoAction()
    listener.run(audio_q)

    tkinter_thread = threading.Thread(target=Face_ui.run_gif.run_tkinter)
    tkinter_thread.start()

    detect_in_row = 0
    sensitivity = 60
    tensor_normalized_output = []
    class_trigger = False
    global _classification_loop

    while _classification_loop:

        if len(audio_q) > 10:  # remove part of stream
            diff = len(audio_q) - 10

            for _ in range(diff):
                audio_q.pop(0)

            fname = action.save(audio_q, get_sample_size)
            tensor_normalized_output = classificator.predict(fname)

        elif len(audio_q) == 10:
            fname = action.save(audio_q, get_sample_size)
            tensor_normalized_output = classificator.predict(fname)

        if class_trigger:
            class_prediction = torch.argmax(dim=-1)
            if class_prediction == 1:
                detect_in_row += 1
                if detect_in_row == sensitivity:
                    action.play()
                    detect_in_row = 0
            else:
                detect_in_row = 0

        time.sleep(5)

        if not tensor_normalized_output == []:
            # this convert from tensor([[-0.05634324  0.47326437  0.8782495   0.03904041]])
            # to [[-0.05634324  0.47326437  0.8782495   0.03904041]] using .numpy
            # finaly [-0.05634324  0.47326437  0.8782495   0.03904041] using .flatten()
            output = tensor_normalized_output.numpy().flatten()
            print(len(output))
            if len(output) == 26:
                # _text_input requres arrays of 26: [1, 2, 3 ... 26]
                Face_ui.run_gif._text_input = output
                Face_ui.run_gif._run_prediction = True

        time.sleep(0.05)

if __name__ == "__main__":

    def signal_handler(signal, frame):
        print("Ctrl+C pressed. Stopping threads...")
        global _classification_loop
        _classification_loop = False
        Face_ui.run_gif._gif_looping = False

    parser = argparse.ArgumentParser(description="demoing the wakeword engine")
    parser.add_argument('--model_class_file', type=str, default="D:\Coding_AI\Voice-Assistant\AudioReaction\wakeword_m.pt", required=False,
                        help='optimized file to load. use optimize_graph.py')
    args = parser.parse_args()


    signal.signal(signal.SIGINT, signal_handler)
    neural_thread = threading.Thread(target = classification_function)
    neural_thread.start()


    while _classification_loop:
        print("Hello")
        time.sleep(1)

