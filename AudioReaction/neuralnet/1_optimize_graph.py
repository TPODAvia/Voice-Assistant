"""Freezes and optimize the model. Use after training."""
import argparse
import torch
from model import LSTM_10

def main(args):
    print("loading model from", args.model_checkpoint)
    model = LSTM_10(input_size=8000, output_size=args.numbers_of_class, hidden_size = 128, num_layers=1) # Instantiate the model
    model.load_state_dict(torch.load(args.model_checkpoint)) # Load the state dictionary
    model.eval()
    print("tracing model...")
    # Prepare an example input
    example_input = torch.randn(1, args.numbers_of_class, 8000)

    # Trace the model
    traced_model = torch.jit.trace(model, example_input)

    print("saving to", args.save_path)
    traced_model.save(args.save_path)
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="optimising the engine")

    parser.add_argument('--numbers_of_class', type=int, default= 4, required=False,
                        help='numbers of class in the /data folder')
    parser.add_argument('--model_checkpoint', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\wakeword.pt", required=False,
                        help='Checkpoint of model to optimize')
    parser.add_argument('--save_path', type=str, default="D:\\Coding_AI\\Voice-Assistant\\AudioReaction\\wakeword_m.pt", required=False,
                        help='path to save optmized model')

    args = parser.parse_args()
    main(args)
