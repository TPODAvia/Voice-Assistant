import whisper
import os
model = whisper.load_model("base")
from pathlib import Path

SCRIPT_DIR = str(Path(__file__).resolve().parent.parent)

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio(f"{SCRIPT_DIR}/StyleTT/Demo/output_scipy.wav")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)