from gtts import gTTS 
import speech_recognition as sr
import requests
import g4f
import os
import sys
import sounddevice as sd
import soundfile as sf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
current_path = os.getcwd()
if current_path.upper() != SCRIPT_DIR.upper():
    print("\n\n")
    print("#"*100)
    print("Current path: " + str(current_path))
    sys.exit('Program can only be run from path ' + SCRIPT_DIR + "\n")

def ask_gpt(messages: list) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=messages
    )
    print(response)
    return response

def is_internet_available():
   try:
       requests.get('http://www.google.com', timeout=3)
       return True
   except (requests.ConnectionError, requests.Timeout):
       return False

def text_to_wav(text: str, voice_lang: str, filename: str):

    mytext = text
    language = voice_lang
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    myobj.save("response_audio.wav") 


if __name__ == "__main__":

    messages = []
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    try:
        while True:
            with microphone as source:
                print("Listening...")
                audio = recognizer.listen(source)

            try:
                if is_internet_available():
                    recognized_data = recognizer.recognize_google(audio, language="ru").lower()
                    print(recognized_data)

                    messages.append({'role': "user", "content": recognized_data})
                    answer = ask_gpt(messages=messages)
                    messages.append({'role': "assistant", "content": answer})
                    text_to_wav(text = answer, voice_lang = "ru", filename = "")
                    data, samplerate = sf.read('response_audio.wav')
                    stream = sd.play(data, samplerate)
                    sd.wait()
                else:
                    print("Internet is not available")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service")
    except KeyboardInterrupt:
        print("Exiting the program")