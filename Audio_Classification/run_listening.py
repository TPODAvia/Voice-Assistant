from run_classification import make_prediction
import sounddevice as sd
import speech_recognition
import numpy as np

recognizer = speech_recognition.Recognizer()
microphone = speech_recognition.Microphone()

with microphone:
    # регулирование уровня окружающего шума
    recognizer.adjust_for_ambient_noise(microphone, duration=2)

with microphone:
    recognized_data = ""

    with speech_recognition.Microphone(sample_rate=16000) as source:
        print("Listening...")
        # playsound('/home/vboxuser/Voice-Assistant/Audio_Classification/output_scipy.wav', False)
        # print("Listening...")
        audio = recognizer.listen(source)
        # recognizer.listen_in_background
        audio_data = audio.get_wav_data()
        data_s16 = np.frombuffer(audio_data, dtype=np.int16, count=len(audio_data)//2, offset=0)
        float_data = data_s16.astype(np.float32, order='C') / 32768.0
        # raw_audio = np.int16(audio_data/np.max(np.abs(audio_data)) * 32767).tobytes()
        # print(audio)
    try:
        #print("Started recognition...")
        # recognized_data = recognizer.recognize_whisper(audio, model="base", language="russian")

        # Sound induced emotion analysis
        sr=16000
        emo_classf = make_prediction(sr, float_data)


    except speech_recognition.UnknownValueError:
        pass

    # в случае проблем с доступом в Интернет происходит выброс ошибки
    except speech_recognition.RequestError:
        print("Check your Internet Connection, please")


fs = 16000  # Sample rate
duration = 0.5 # duration in second
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

# print(emo_classf)