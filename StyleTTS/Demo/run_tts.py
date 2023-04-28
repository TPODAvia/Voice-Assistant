# load packages
import sys
import yaml
from munch import Munch
import numpy as np
import torch
import torchaudio
import librosa
from scipy.io import wavfile
import phonemizer
from random import SystemRandom

sys.path.append("/home/vboxuser/Voice-Assistant/StyleTTS")
from models import build_model, load_ASR_models, load_F0_models
from utils import *

sys.path.append("/home/vboxuser/Voice-Assistant/StyleTTS/Demo/hifi-gan")

import glob
import os
import json
import torch
from attrdict import AttrDict
from vocoder import Generator
import librosa
import numpy as np
import torchaudio

class TextCleaner:
    def __init__(self, dummy=None):
        
        _pad = "$"
        _punctuation = ';:,.!?¡¿—…"«»“” '
        _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        _letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"


        # Export all symbols:
        symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)

        dicts = {}
        for i in range(len((symbols))):
            dicts[symbols[i]] = i

        self.word_index_dictionary = dicts

    def __call__(self, text):
        indexes = []
        for char in text:
            try:
                indexes.append(self.word_index_dictionary[char])
            except KeyError:
                print(char)
        return indexes

def length_to_mask(lengths):
    mask = torch.arange(lengths.max()).unsqueeze(0).expand(lengths.shape[0], -1).type_as(lengths)
    mask = torch.gt(mask+1, lengths.unsqueeze(1))
    return mask

def preprocess(wave):
    wave_tensor = torch.from_numpy(wave).float()

    to_mel = torchaudio.transforms.MelSpectrogram(
    n_mels=80, n_fft=2048, win_length=1200, hop_length=300)

    mel_tensor = to_mel(wave_tensor)
    mean, std = -4, 4
    mel_tensor = (torch.log(1e-5 + mel_tensor.unsqueeze(0)) - mean) / std
    return mel_tensor

def compute_style(ref_dicts, model, device):

    keys_list = list(ref_dicts.keys())
    emotion = keys_list[0] # Angry Happy Sad Surprise etc

    path = '/home/vboxuser/Voice-Assistant/StyleTTS/Emotion/' + emotion + '/evaluation/'
    wav_filenames = [filename for filename in glob.glob(os.path.join(path, '*.wav'))]

    cryptogen = SystemRandom()

    reference_embeddings = {}
    for key, path in ref_dicts.items():
        wave, sr = librosa.load(wav_filenames[cryptogen.randrange(len(wav_filenames))], sr=24000)
        audio, index = librosa.effects.trim(wave, top_db=30)
        if sr != 24000:
            audio = librosa.resample(audio, sr, 24000)
        mel_tensor = preprocess(audio).to(device)

        with torch.no_grad():
            ref = model.style_encoder(mel_tensor.unsqueeze(1))
        reference_embeddings[key] = (ref.squeeze(1), audio)
    
    return reference_embeddings

def load_checkpoint(filepath, device):
    assert os.path.isfile(filepath)
    print("Loading '{}'".format(filepath))
    checkpoint_dict = torch.load(filepath, map_location=device)
    print("Complete.")
    return checkpoint_dict

def scan_checkpoint(cp_dir, prefix):
    pattern = os.path.join(cp_dir, prefix + '*')
    cp_list = glob.glob(pattern)
    if len(cp_list) == 0:
        return ''
    return sorted(cp_list)[-1]

def from_pretrained(device):

    textclenaer = TextCleaner()

    cp_g = scan_checkpoint("/home/vboxuser/Voice-Assistant/StyleTTS/Vocoder/LibriTTS/", 'g_')

    config_file = os.path.join(os.path.split(cp_g)[0], '/home/vboxuser/Voice-Assistant/StyleTTS/Vocoder/LibriTTS/config.json')
    with open(config_file) as f:
        data = f.read()
    json_config = json.loads(data)
    h = None
    h = AttrDict(json_config)

    device = torch.device(device)
    generator = Generator(h).to(device)

    state_dict_g = load_checkpoint(cp_g, device)
    generator.load_state_dict(state_dict_g['generator'])
    generator.eval()
    generator.remove_weight_norm()

    # load StyleTTS
    model_path = "/home/vboxuser/Voice-Assistant/StyleTTS/Models/LJSpeech/epoch_2nd_00008.pth"
    model_config_path = "/home/vboxuser/Voice-Assistant/StyleTTS/Models/LJSpeech/config.yml"

    config = yaml.safe_load(open(model_config_path))

    # load pretrained ASR model
    ASR_config = config.get('ASR_config', False)
    ASR_path = config.get('ASR_path', False)
    text_aligner = load_ASR_models(ASR_path, ASR_config)

    # load pretrained F0 model
    F0_path = config.get('F0_path', False)
    pitch_extractor = load_F0_models(F0_path)

    model = build_model(Munch(config['model_params']), text_aligner, pitch_extractor)

    params = torch.load(model_path, map_location='cpu')
    params = params['net']
    for key in model:
        if key in params:
            if not "discriminator" in key:
                print('%s loaded' % key)
                model[key].load_state_dict(params[key])
    _ = [model[key].eval() for key in model]
    _ = [model[key].to(device) for key in model]
    

    return model, generator, textclenaer


def main(text, ref_dicts, model, generator, textclenaer, device, global_phonemizer):

    reference_embeddings = compute_style(ref_dicts, model, device)

    # tokenize
    ps = global_phonemizer.phonemize([text])
    tokens = textclenaer(ps[0])
    tokens.insert(0, 0)
    tokens.append(0)
    tokens = torch.LongTensor(tokens).to(device).unsqueeze(0)

    converted_samples = {}

    with torch.no_grad():
        input_lengths = torch.LongTensor([tokens.shape[-1]]).to(device)
        m = length_to_mask(input_lengths).to(device)
        t_en = model.text_encoder(tokens, input_lengths, m)
            
        for key, (ref, _) in reference_embeddings.items():
            
            s = ref.squeeze(1)
            style = s
            
            d = model.predictor.text_encoder(t_en, style, input_lengths, m)

            x, _ = model.predictor.lstm(d)
            duration = model.predictor.duration_proj(x)
            pred_dur = torch.round(duration.squeeze()).clamp(min=1)
            
            pred_aln_trg = torch.zeros(input_lengths, int(pred_dur.sum().data))
            c_frame = 0
            for i in range(pred_aln_trg.size(0)):
                pred_aln_trg[i, c_frame:c_frame + int(pred_dur[i].data)] = 1
                c_frame += int(pred_dur[i].data)

            # encode prosody
            en = (d.transpose(-1, -2) @ pred_aln_trg.unsqueeze(0).to(device))
            style = s.expand(en.shape[0], en.shape[1], -1)

            F0_pred, N_pred = model.predictor.F0Ntrain(en, s)

            out = model.decoder((t_en @ pred_aln_trg.unsqueeze(0).to(device)), 
                                    F0_pred, N_pred, ref.squeeze().unsqueeze(0))


            c = out.squeeze()
            y_g_hat = generator(c.unsqueeze(0))
            y_out = y_g_hat.squeeze()
            
            converted_samples[key] = y_out.cpu().numpy()

    waves = []
    for key, wave in converted_samples.items():
        waves = wave
    
    return waves

def save_wave_scipy(filename, audio_data, sample_rate):
    audio_data = (audio_data * (2**15 - 1) // np.max(np.abs(audio_data))).astype(np.int16)
    wavfile.write(filename, sample_rate, audio_data)

if __name__=="__main__":


    # load phonemizer
    global_phonemizer = phonemizer.backend.EspeakBackend(language='ru', preserve_punctuation=True,  with_stress=True)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Happy Sad Angry Surprise Neutral
    ref_dicts = {}
    ref_dicts["Happy"] = "Some comments"

    # synthesize a text
    text = ''' Приближаются долгожданные майские праздники. '''

    model, generator, textclenaer = from_pretrained(device)

    save_wave_scipy('output_scipy.wav', main(text, ref_dicts, model, generator, textclenaer, device, global_phonemizer), 24000)
