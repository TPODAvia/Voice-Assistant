"""the interface to interact with wakeword model"""
import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# current_path = os.getcwd()
# if current_path.upper() != SCRIPT_DIR.upper():
#     print("\n\n")
#     print("#"*100)
#     print("Current path: " + str(current_path))
#     sys.exit('Program can only be run from path ' + SCRIPT_DIR)

sys.path.append(os.path.dirname(SCRIPT_DIR) + "/Face_ui")

import pyaudio
import threading
import time
import argparse
import wave
import torchaudio
import torch
import signal
import run_gif

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
        while True:
            data = self.stream.read(self.chunk , exception_on_overflow=False)
            queue.append(data)
            time.sleep(0.01)

    def run(self, queue):
        thread = threading.Thread(target=self.listen, args=(queue,), daemon=True)
        thread.start()
        print("\nWake Word Engine is now listening... \n")

class ClassificationEngine:

    def __init__(self, model_lstm_file):
        self.listener = Listener(sample_rate=8000, record_seconds=1)
        self.model = torch.jit.load(model_lstm_file)
        self.model.eval().to('cpu')  #run on cpu
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.audio_q = list()
        signal.signal(signal.SIGINT, self.signal_handler)

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
            waveform, sample_rate = torchaudio.load(fname)  # don't normalize on train
            tensor = waveform.to(self.device)
            model_output = self.model(tensor.unsqueeze(0))

            # for classification result use this
            # tensor.argmax(dim=-1)

            # this normalized all numbers to [0...1]
            normalized_output = torch.nn.functional.normalize(model_output, p=2, dim=-1)

            # this convert from tensor([[-0.05634324  0.47326437  0.8782495   0.03904041]])
            # to [[-0.05634324  0.47326437  0.8782495   0.03904041]] using .numpy
            # final [-0.05634324  0.47326437  0.8782495   0.03904041] using .flatten()
            self.output = normalized_output.numpy().flatten()
            # print(output)
            return self.output

    def inference_loop(self, action):
        while True:
            if len(self.audio_q) > 10:  # remove part of stream
                diff = len(self.audio_q) - 10
                for _ in range(diff):
                    self.audio_q.pop(0)
                action(self.predict(self.audio_q))
            elif len(self.audio_q) == 10:
                action(self.predict(self.audio_q))
            time.sleep(0.05)

    def run(self, action):
        self.listener.run(self.audio_q)
        thread = threading.Thread(target=self.inference_loop,
                                    args=(action,), daemon=True)
        thread.start()

        # Run the tkinter event loop in a separate thread
        run_gif.text_input = [  1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ]
        run_gif.run_prediction = False    

        # Run the tkinter event loop in a separate thread
        tkinter_thread = threading.Thread(target=run_gif.run_tkinter)
        tkinter_thread.start()
        run_gif.my_event = True

        time.sleep(5)
        try:
            while run_gif.my_event:
                # Your other code goes here
                print("Executing other code...")

                # run_gif.text_input = self.output
                run_gif.text_input = [  0,0,0,1, 0,0,0,0, 0,0,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0  ] #26
                run_gif.run_prediction = True
                time.sleep(10)

        except KeyboardInterrupt:
            print("Caught keyboard interrupt, terminating threads")
            sys.exit(0)

    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        run_gif.my_event = False
        sys.exit(0)

class DemoAction:
    """This demo action will just randomly say Arnold Schwarzenegger quotes
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

        print(prediction)
        # if prediction == 1:   # change this to the class label you're interested in
        #     self.detect_in_row += 1
        #     if self.detect_in_row == self.sensitivity:
        #         self.play()
        #         self.detect_in_row = 0
        # else:
        #     self.detect_in_row = 0

    def play(self):
        filename = self.random.choice(self.arnold_mp3)
        try:
            print("playing", filename)
            self.subprocess.check_output(['play', '-v', '.1', filename , '-t', 'alsa'])
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="demoing the wakeword engine")
    parser.add_argument('--model_lstm_file', type=str, default="D:\Coding_AI\Voice-Assistant\AudioReaction\wakeword_m.pt", required=False,
                        help='optimized file to load. use optimize_graph.py')

    args = parser.parse_args()
    wakeword_engine = ClassificationEngine(args.model_lstm_file)
    action = DemoAction(sensitivity=60)

    print("""\n*** Make sure you have sox installed on your system for the demo to work!!!
    If you don't want to use sox, change the play function in the DemoAction class
    in engine.py module to something that works with your system.\n
    """)
    # action = lambda x: print(x)
    wakeword_engine.run(action)

    threading.Event().wait()
