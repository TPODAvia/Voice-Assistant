"""Training script"""

import os
import argparse
import torch
import torch.nn.functional as F
import torch.optim as optim
from dataset import CustomAudioDataset, collate_fn, number_of_correct, get_likely_index
from model import LSTM_10
import torchaudio
from tqdm import tqdm
import sys

def test(device, model, epoch, test_loader, transform):
    model.eval()
    correct = 0
    for data, target in test_loader:

        data = data.to(device)
        target = target.to(device)

        # apply transform and model on whole batch directly on device
        data = transform(data)
        output = model(data)

        pred = get_likely_index(output)
        correct += number_of_correct(pred, target)

        # update progress bar
        # pbar.update(pbar_update)

    print(f"\nTest Epoch: {epoch}\tAccuracy: {correct}/{len(test_loader.dataset)} ({100. * correct / len(test_loader.dataset):.0f}%)\n")

def train(device, model, epoch, log_interval, train_loader, transform, optimizer):
    model.train()
    print("\n")
    for batch_idx, (data, target) in enumerate(train_loader):

        data = data.to(device)
        target = target.to(device)

        # apply transform and model on whole batch directly on device
        data = transform(data)
        output = model(data)

        # negative log-likelihood for a tensor of size (batch x 1 x n_output)
        loss = F.nll_loss(output.squeeze(), target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # print training stats
        if batch_idx % log_interval == 0:
            print(f"Train Epoch: {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)} ({100. * batch_idx / len(train_loader):.0f}%)]\tLoss: {loss.item():.6f}")
            # update progress bar
        # pbar.update(pbar_update)

def main(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_set = CustomAudioDataset(args.train_data_txt, args.audio_path)
    test_set = CustomAudioDataset(args.test_data_txt, args.audio_path)

    waveform, sample_rate, label, speaker_id, utterance_number = train_set[0] 

    print("\n The train samle data set:")
    print(train_set[0]) # (tensor([[0.0234, 0.0234, 0.0234,  ..., 0.0234, 0.0156, 0.0156]]), 11025, '2', 'maymun', 0)

    # Let’s find the list of labels available in the dataset.
    labels = sorted(list(set(datapoint[2] for datapoint in train_set)))
    print("\n All labels are sorted:")
    print(labels) # ['0', '1', '2', '3']


    if device == "cuda":
        num_workers = 1
        pin_memory = True
    else:
        num_workers = 0
        pin_memory = False

    batch_size = 256

    train_loader = torch.utils.data.DataLoader(
        train_set,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=lambda batch: collate_fn(batch, labels),
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    test_loader = torch.utils.data.DataLoader(
        test_set,
        batch_size=batch_size,
        shuffle=False,
        drop_last=False,
        collate_fn=lambda batch: collate_fn(batch, labels),
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    model = LSTM_10(input_size=8000, output_size=len(labels), hidden_size = 128, num_layers=1)
    model.to(device)

    print("\n Model Architecture:")
    print("#"*80)
    print(model)
    print("#"*80)
    print("\n")


    def count_parameters(model):
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    n = count_parameters(model)
    print("Number of parameters: %s" % n)   

    # reduce the learning after 20 epochs by a factor of 10
    optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=0.0001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.1)


    log_interval = 400
    n_epoch = 6

    # pbar_update = 1 / (len(train_loader) + len(test_loader))
    # losses = []
    # pbar = 

    # print(train_loader.shape)
    # The transform needs to live on the same device as the model and the data.
    new_sample_rate = 8000
    transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=new_sample_rate)
    transform = transform.to(device)
    with tqdm(total=n_epoch) as pbar:
        for epoch in range(1, n_epoch + 1):
            train(device, model, epoch, log_interval, train_loader, transform, optimizer)
            test(device, model, epoch, test_loader, transform)
            scheduler.step()

            # saves checkpoint if metrics are better than last
            if args.save_checkpoint_path:
                    torch.save(model.state_dict(), os.path.join(args.save_checkpoint_path, 'wakeword.pt'))

    print("Done Training...")
    print("Best Model Saved to", args.save_checkpoint_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classification Training Script")
    parser.add_argument('--save_checkpoint_path',   type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction", help='Path to save the best checkpoint')
    parser.add_argument('--audio_path',             type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data", required=False, help='path to all audio file')
    parser.add_argument('--train_data_txt',         type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data\\train.txt", required=False, help='path to train data txt file')
    parser.add_argument('--test_data_txt',          type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\scripts\\data\\test.txt", required=False, help='path to test data txt file')

    args = parser.parse_args()

    main(args)
