import speech_recognition
import whisper

# Load the Whisper model
whisper_model = whisper.load_model("tiny")

# Initialize the recognizer
recognizer = speech_recognition.Recognizer()

with speech_recognition.Microphone() as source:
    print("Listening...")
    audio = recognizer.record(source, duration=5)
    # audio_data = audio.get_wav_data()

# Recognize the speech using the Whisper recognizer
try:
    text = recognizer.recognize_whisper(audio)
    print(f"Recognized text: {text}")
except speech_recognition.UnknownValueError:
    print("Whisper could not understand the audio")
except speech_recognition.RequestError as e:
    print(f"Could not request results from Whisper; {e}")
