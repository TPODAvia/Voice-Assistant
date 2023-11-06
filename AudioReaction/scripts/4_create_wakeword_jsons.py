"""Utility script to create training json file for wakeword.

    There should be two directories. one that has all of the 0 labels
    and one with all the 1 labels
"""
import os
import argparse
import json
import random


def main(args):
    data = []
    root_dir = args.data_dir
    percent = args.percent
    subdirs = [os.path.join(root_dir, d) for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    for idx, subdir in enumerate(subdirs):
        files = os.listdir(subdir)
        for file in files:
            data.append({
                "key": os.path.join(subdir, file),
                "label": idx
            })
    random.shuffle(data)

    f = open(args.save_json_path +"/"+ "train.json", "w")
    
    with open(args.save_json_path +"/"+ 'train.json','w') as f:
        d = len(data)
        i=0
        while(i<int(d-d/percent)):
            r=data[i]
            line = json.dumps(r)
            f.write(line + "\n")
            i = i+1
    
    f = open(args.save_json_path +"/"+ "test.json", "w")

    with open(args.save_json_path +"/"+ 'test.json','w') as f:
        d = len(data)
        i=int(d-d/percent)
        while(i<d):
            r=data[i]
            line = json.dumps(r)
            f.write(line + "\n")
            i = i+1
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Utility script to create training json file for wakeword.
    """
    )
    parser.add_argument('--data_dir', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data", required=False,
                        help='root directory of clips with labels')
    parser.add_argument('--save_json_path', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data", required=False,
                        help='path to save json file')
    parser.add_argument('--percent', type=int, default=10, required=False,
                        help='percent of clips put into test.json instead of train.json')
    args = parser.parse_args()

    main(args)
