import time
import numpy as np
import os
import sys
import re
import threading
import argparse
import pyaudio
import speech_recognition

# sys.path.append(os.path.dirname(SCRIPT_DIR) + "/AudioReaction")
import engine
import signal
import sys
_interrupted = True
def signal_handler(signal, frame):
    print("Ctrl+C pressed. Stopping threads...")
    _interrupted = False
    engine.run_gif.my_event = False
    stop_event.set()
    engine_thread.join()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
parser=argparse.ArgumentParser()

parser.add_argument("--model_path", type=str, default="", required=False, 
                    help="The path of a specific model to load")

parser.add_argument('--model_lstm_file', type=str, default="D:\Coding_AI\Voice-Assistant\AudioReaction\wakeword_m.pt", required=False,
                    help='optimized file to load. use optimize_graph.py')
args=parser.parse_args()

# stop_event = threading.Event()


def run_engine(stop_event):
    wakeword_engine = engine.ClassificationEngine(args.model_lstm_file)
    action = engine.DemoAction(sensitivity=60)
    wakeword_engine.run(action)
    while not stop_event.is_set():
        wakeword_engine.run(action)

# def signal_handler(signal, frame):
#     global stop_threads
#     stop_threads = True
#     stop_event.set()

print("main start")
engine.run_gif.my_event = True
if __name__ == "__main__":

    stop_event = threading.Event()
    # Run the UI and audio classification
    engine_thread = threading.Thread(target=run_engine, args=(stop_event,))
    _interrupted = True

    try:
        engine_thread.start()
        while _interrupted:

            # print("_recognized_data: " + str(_recognized_data))
            # print(_recognized_data)
            voice_input_str = "Helllo+++++++++++++++++++++++++++++++++++++++++++++++"
            print(voice_input_str)
            
            time.sleep(5)

    except KeyboardInterrupt:
        _interrupted = False
        stop_event.set()
        engine_thread.join()
        print("Thread finished task, exiting")
        engine.run_gif.my_event = False
        sys.exit()