import pandas as pd
# load phonemizer
import phonemizer
global_phonemizer = phonemizer.backend.EspeakBackend(language='ru', preserve_punctuation=True,  with_stress=True)

def phonemize(global_phonemizer, text):
    return global_phonemizer.phonemize([text])[0]


# Read the JSON file into a DataFrame
with open('D:\\Datasets\\ruls_data\\dev\\manifest.json', 'r', encoding='utf-8') as json_file:
    data = pd.read_json(json_file, lines=True)

# Extract the required columns
extracted_data = data[['audio_filepath', 'text_no_preprocessing']]

# Add a new column with constant value 0
extracted_data['constant'] = 0

# Save the extracted data to a TXT file with the specified format and UTF-8 encoding
with open('output.txt', 'w', encoding='utf-8') as output_file:
    for index, row in extracted_data.iterrows():
        output_file.write(f"{row['audio_filepath']}|{phonemize(global_phonemizer, row['text_no_preprocessing'])}|{row['constant']}\n")