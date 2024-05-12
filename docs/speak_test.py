import os
import subprocess
import numpy as np
import sounddevice as sd
import soundfile as sf
from audioplayer import AudioPlayer
from pathlib import Path
from colorama import Fore, Back, Style

SCRIPT_DIR = str(Path(__file__).resolve().parent.parent)
# Path to the WAV file
wavfile = SCRIPT_DIR + "/Irene-Voice-Assistant/media/bit.wav"

# Test 1: Play using AudioPlayer
def test_audio_player():
    print(Fore.GREEN + "Testing AudioPlayer..." + Style.RESET_ALL)
    player = AudioPlayer(wavfile)
    player.play(block=True)
    print("AudioPlayer test completed.")

# Test 2: Play using subprocess and aplay
def test_aplay():
    print(Fore.GREEN + "Testing aplay..."  + Style.RESET_ALL)
    print(Style.RESET_ALL)
    subprocess.call(f"aplay {wavfile}", shell=True)
    print("aplay test completed.")

# Test 3: Play using sounddevice and soundfile
def test_sounddevice():
    print(Fore.GREEN + "Testing sounddevice..." + Style.RESET_ALL)
    data, fs = sf.read(wavfile, dtype='float32')
    print(f"{len(data)} : {fs}")
    # Fix to prevent cut-offs at the end of playback
    sd.play(data, fs)
    sd.wait()
    print("sounddevice test completed.")

# Run all tests
if __name__ == "__main__":
    print("-"*80)
    test_audio_player()
    print("-"*80)
    test_aplay()
    print("-"*80)
    test_sounddevice()
    print("-"*80)
