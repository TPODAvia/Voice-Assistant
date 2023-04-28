import json

def read_text_and_create_json(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as fout:
        for line in lines:
            line_dict = {"text": line.strip()}
            json.dump(line_dict, fout, ensure_ascii=False)
            fout.write("\n")

input_file = "this_output.txt"
output_file = "output2.json"
read_text_and_create_json(input_file, output_file)