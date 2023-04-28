import os
from simpletransformers.classification import MultiLabelClassificationModel
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Model Start++++++++++++++++++++++++++++++++++++++++++++++++++++")
model = MultiLabelClassificationModel("roberta", SCRIPT_DIR + "/outputs/checkpoint-9-epoch-3/", num_labels=26, use_cuda=False)

print("Model Start Predict++++++++++++++++++++++++++++++++++++++++++++++++++++")
predictions, raw_outputs = model.predict(['I Love you so much! I Love you so much!'])

print("Prediction: ", predictions)

print("raw_outputs: ", raw_outputs)