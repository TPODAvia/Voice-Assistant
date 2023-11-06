import os
import argparse
from pydub import AudioSegment
from pydub.utils import make_chunks
import glob

def main(args):
    audio_files = glob.glob(os.path.join(args.audio_file_name, "*.wav"))
    count = 0
    for audio_file in audio_files:
        count +=1
        # print(count)
        # print(audio_file)
        audio = AudioSegment.from_file(audio_file)
        length = args.seconds * 1000 # this is in miliseconds
        chunks = make_chunks(audio, length)
        for i, chunk in enumerate(chunks):
            if i == len(chunks) - 1:
                break
            base_name = os.path.basename(audio_file).rsplit("_", 1)[0]
            name = "{}_{}_chunk_{}.wav".format(base_name, count, i)
            wav_path = os.path.join(args.save_path, name)
            chunk.export(wav_path, format="wav")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="script to split audio files into chunks")
    parser.add_argument('--seconds', type=int, default=1,
                        help='if set to None, then will record forever until keyboard interrupt')
    parser.add_argument('--audio_file_name', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data_s\\3", required=False,
                        help='name of audio file')
    parser.add_argument('--save_path', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data\\3", required=False,
                        help='full path to to save data. i.e. /to/path/saved_clips/')

    args = parser.parse_args()

    main(args)
