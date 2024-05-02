"""classification model"""
import torch
import torch.nn as nn
from torchviz import make_dot

class LSTM_10(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTM_10, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        # self.fc2 = nn.Linear(hidden_size, hidden_size)
        # self.fc = nn.Linear(hidden_size, output_size)
        self.fc1 = nn.Linear(self.hidden_size, int(self.hidden_size/2))
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(int(self.hidden_size/2), int(self.hidden_size/2))
        self.fc3 = nn.Linear(int(self.hidden_size/2), output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device) 
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0)) 
        # out = self.fc(out[:, -1, :]) 
        out = self.relu(self.fc1(out[:, -1, :]))
        out = self.relu(self.fc2(out))
        out = self.fc3(out) 
        return out
    
def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

if __name__ == '__main__':

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)

    model = LSTM_10(input_size=16000, output_size=5, hidden_size = 128, num_layers=1)
    model.to(device)

    print("\n")
    print("#"*60 + "\n")
    print(model)
    print("\n" + "#"*60)
    print("\n")


    dummy_input = torch.randn(1, 5, 16000)
    out = model(dummy_input)
    make_dot(out, params=dict(model.named_parameters())).render("model_graph", format="png")

    n = count_parameters(model)
    print("Number of parameters: %s" % n)
