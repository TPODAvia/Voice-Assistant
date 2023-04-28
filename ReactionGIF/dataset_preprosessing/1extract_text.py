import json
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.dirname(SCRIPT_DIR) + '/ReactionGIF_EN.json', 'r') as json_file, open('output.json', 'w') as output_file:
    for line in json_file:
        data = json.loads(line.strip())
        text = data['text']
        new_data = {'XOZASDFGHJ': text}
        json.dump(new_data, output_file)
        output_file.write('\n') # Add newline character to separate li