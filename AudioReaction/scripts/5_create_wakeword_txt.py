import os
import argparse
import random

def main(args):
    data = []
    root_dir = args.data_dir
    percent = args.percent
    subdirs = [os.path.join(root_dir, d) for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    for idx, subdir in enumerate(subdirs):
        files = os.listdir(subdir)
        for file in files:
            # Change the data structure to match the desired format
            # data.append(os.path.join(subdir, file))
            relative_path = os.path.relpath(os.path.join(subdir, file), root_dir)
            relative_path = relative_path.replace('\\', '/')
            data.append(relative_path)
            data.append(relative_path)

    random.shuffle(data)

    with open(args.save_txt_path +"/"+ "train.txt", "w") as f:
        d = len(data)
        i=0
        while(i<int(d-d/percent)):
            line = data[i] + "\n"
            f.write(line)
            i = i+1

    with open(args.save_txt_path +"/"+ 'test.txt', 'w') as f:
        d = len(data)
        i=int(d-d/percent)
        while(i<d):
            line = data[i] + "\n"
            f.write(line)
            i = i+1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Utility script to create training json file for wakeword.
    """
    )
    parser.add_argument('--data_dir', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data", required=False,
                        help='root directory of clips with labels')
    parser.add_argument('--save_txt_path', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data", required=False,
                        help='path to save txt file')
    parser.add_argument('--percent', type=int, default=10, required=False,
                        help='percent of clips put into test.json instead of train.txt')
    args = parser.parse_args()

    main(args)
