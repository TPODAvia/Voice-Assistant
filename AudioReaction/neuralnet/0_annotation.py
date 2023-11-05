# import os
# make sure to install graphviz https://graphviz.org/download/
import torch
from model import LSTMWakeWord
from torchviz import make_dot

model = LSTMWakeWord(num_classes=8, feature_size=40, hidden_size=128, num_layers=1, dropout=0.1, bidirectional=False)

dummy_input = torch.randn(1, 128, 40)
out = model(dummy_input)
dot = make_dot(out, params=dict(list(model.named_parameters())))
dot.render("lstm_model_graph", format="png")

print("\n")
print("#"*70)
print("\n")
print(model)
print("\n")
print("#"*70)
print("\n")