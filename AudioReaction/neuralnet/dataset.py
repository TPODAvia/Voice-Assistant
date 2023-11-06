"""download and/or process data"""
from torch.utils.data import Dataset
import torchaudio
import torch
import os

class CustomAudioDataset(Dataset):
    def __init__(self, txt_file, root_dir):
        self.txt_file = txt_file
        self.root_dir = root_dir

        with open(txt_file, 'r') as file:
            lines = file.readlines()

        self.filepaths = [os.path.join(root_dir, line.split()[0]) for line in lines]

        self.labels = []
        self.utterance_number = []
        # print(len(lines))
        for line in lines:
            new_split_line, number = line.split("_nohash_")
            label = new_split_line.split("/")
            parts = number.split('.')

            self.utterance_number.append(int(parts[0]))
            self.labels.append(label[0])


    def __len__(self):
        return len(self.filepaths)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        audio_file = self.filepaths[idx]
        label = self.labels[idx]
        utterance_number = self.utterance_number[idx]

        # Load the audio file
        waveform, sample_rate = torchaudio.load(audio_file)

        # Extract speaker_id and utterance_number from filename
        speaker_id, _ = os.path.basename(audio_file).split("_")[0:2]

        # sample = {
        #     # 'audio': audio_file,
        #     'waveform': waveform,
        #     'sample_rate': sample_rate,
        #     'label': label,
        #     'speaker_id': speaker_id,
        #     'utterance_number': len(utterance_number),
        # }

        # return sample
        return waveform, sample_rate, label, speaker_id, utterance_number

def pad_sequence(batch):
    # Make all tensor in a batch the same length by padding with zeros
    batch = [item.t() for item in batch]
    batch = torch.nn.utils.rnn.pad_sequence(batch, batch_first=True, padding_value=0.)
    return batch.permute(0, 2, 1)


def collate_fn(batch, labels):

    # A data tuple has the form:
    # waveform, sample_rate, label, speaker_id, utterance_number

    tensors, targets = [], []

    # Gather in lists, and encode labels as indices
    for waveform, _, label, *_ in batch:
        tensors += [waveform]
        targets += [label_to_index(label, labels)]

    # Group the list of tensors into a batched tensor
    tensors = pad_sequence(tensors)
    targets = torch.stack(targets)

    return tensors, targets

def label_to_index(word, labels):
    # Return the position of the word in labels
    return torch.tensor(labels.index(word))


def index_to_label(index, labels):
    # Return the word corresponding to the index in labels
    # This is the inverse of label_to_index
    return labels[index]

def number_of_correct(pred, target):
    # count number of correct predictions
    return pred.squeeze().eq(target).sum().item()


def get_likely_index(tensor):
    # find most likely label index for each element in the batch
    return tensor.argmax(dim=-1)


if __name__ == '__main__':

    train_set = CustomAudioDataset("D:\\Coding_AI\\Voice-Assistant\AudioReaction\\speech_commands_v0.02\\testing_list.txt", "D:\\Coding_AI\\Voice-Assistant\AudioReaction\\speech_commands_v0.02")
    test_set = CustomAudioDataset("D:\\Coding_AI\\Voice-Assistant\AudioReaction\\speech_commands_v0.02\\validation_list.txt", "D:\\Coding_AI\\Voice-Assistant\AudioReaction\\speech_commands_v0.02")

    # this is working right now woth output: {'audio':"audio path ": '1.wav'}
    waveform, sample_rate, label, speaker_id, utterance_number = train_set[0] 
    print(train_set[0] )
    labels = sorted(list(set(datapoint[2] for datapoint in train_set)))

    word_start = "yes"
    index = label_to_index(word_start)
    word_recovered = index_to_label(index, labels)

    print(word_start, "-->", index, "-->", word_recovered)