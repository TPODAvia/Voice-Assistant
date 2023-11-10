import sounddevice as sd
import soundfile as sf

data, samplerate = sf.read('response_audio.wav')
stream = sd.play(data, samplerate)
sd.wait()