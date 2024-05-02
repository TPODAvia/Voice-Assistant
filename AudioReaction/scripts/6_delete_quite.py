import os
from pydub import AudioSegment
from pydub.utils import mediainfo

def average_db_level(filename):
    """Calculate the average dB level of an audio file."""
    audio = AudioSegment.from_file(filename)
    return audio.dBFS

def delete_low_volume_files(directory, threshold_db):
    """Delete files with an average dB level below the specified threshold."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                db_level = average_db_level(filepath)
                # print(db_level)
                if db_level == float('-inf'):
                    os.remove(filepath)
                    print(f"Deleted {filepath} because it is silent or unprocessable.")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

# Usage
directory_to_check = 'D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data'
db_threshold = -10  # dB level threshold, adjust according to your needs
delete_low_volume_files(directory_to_check, db_threshold)
