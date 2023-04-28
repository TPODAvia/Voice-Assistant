# -*- coding: utf-8 -*-

import os, random
import torch
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# reproducibility
seed = 42
os.environ['PYTHONHASHSEED'] = str(seed)
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)

file = os.path.dirname(SCRIPT_DIR) + '/ReactionGIF.json'
df = pd.read_json(file, lines=True)
train_data, test_data = train_test_split(df, random_state=43, test_size=0.1)
train_data = train_data.copy()
test_data = test_data.copy()
train_data['label'] = pd.Categorical(train_data['label'])
train_data['labels'] = train_data['label'].cat.codes
categories = train_data['label'].cat.categories

test_data['label'] = pd.Categorical(test_data['label'], categories=categories)
test_data['labels'] = test_data['label'].cat.codes
def report(gold, pred):
    print(classification_report(gold, pred, digits=3))
    acc = accuracy_score(gold, pred)
    p = precision_score(gold, pred, average='weighted')
    r = recall_score(gold, pred, average='weighted')
    f1 = f1_score(gold, pred, average='weighted')
    print(f'{acc*100:.1f} & {p*100:.1f} & {r*100:.1f} & {f1*100:.1f}')

"""#Majority"""

majority = train_data['labels'].value_counts().keys()[0]
test_data['pred'] = majority
report(test_data['labels'], test_data['pred'])

"""#TFIDF"""

# from sklearn.feature_extraction.text import TfidfVectorizer

# vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=1000, stop_words='english') # using default parameters
# vectorizer.fit(train_data['text'])
# train_X = vectorizer.transform(train_data['text'])
# test_X = vectorizer.transform(test_data['text'])
# print(train_X.shape, test_X.shape)

# """#LogisticRegressionCV

# """

# from sklearn.linear_model import LogisticRegressionCV


# model = LogisticRegressionCV(Cs=3, cv=5, verbose=1, max_iter=1000, n_jobs=-1)
# model.fit(train_X, train_data['labels'])
# pred_y = model.predict(test_X)
# report(test_data['labels'], pred_y)

import sys
train_df = pd.DataFrame(train_data['text'])

list = []
for i in range(0,train_data['labels'].shape[0]):
    arr0 = [0] * len(categories) # arrays of len(categories)=43 zeros
    s = train_data['labels'].values[i]
    arr0[s] = 1
    list.append(arr0)

train_df.reset_index(drop=True, inplace=True)
train_df['labels'] = pd.Series(list)

# Get the total number of rows in the DataFrame
total_rows = train_df.shape[0]

# Calculate the index of the row up to which all rows need to be preserved
preserve_index = total_rows - 18000

# Drop all the rows after the specified index
train_df.drop(train_df.index[preserve_index:], inplace=True)

print(train_df)
print(train_df.shape)
print(len(categories))
# sys.exit()


"""#RoBERTa"""

# !pip install tqdm
# !pip install transformers
# !pip install simpletransformers
# !pip install tensorboardx

from simpletransformers.classification import (
    MultiLabelClassificationModel, MultiLabelClassificationArgs
)

# Optional model configuration
model_args = MultiLabelClassificationArgs(num_train_epochs=1, use_multiprocessing=False, use_multiprocessing_for_evaluation=False)

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Create a MultiLabelClassificationModel
model = MultiLabelClassificationModel(
    "roberta",
    "roberta-base",
    num_labels=43,
    args=model_args,
    use_cuda=False
)

# Train the model
model.train_model(train_df, args={
    'fp16': False,
    'overwrite_output_dir': True,
    'train_batch_size': 32,
    "eval_batch_size": 32,
    'max_seq_length': 96,
    'num_train_epochs': 3
})

# Evaluate the model
# result, model_outputs, wrong_predictions = model.eval_model(
#     eval_df
# )

# Make predictions with the model
predictions, raw_outputs = model.predict(["I hate this school homework dumb shit"])

print("Prediction: ", predictions)

print("raw_outputs: ", raw_outputs)