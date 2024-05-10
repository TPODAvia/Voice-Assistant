import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from pathlib import Path

os.environ['PYTHONHTTPSVERIFY'] = '0'
SCRIPT_DIR = str(Path(__file__).resolve().parent.parent)
cache_dir = SCRIPT_DIR+ "/Models/"

# Load the tokenizer and model from the Hugging Face Hub
tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-medium', cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained('tinkoff-ai/ruDialoGPT-medium', cache_dir=cache_dir)

# Prepare the text input for the model
inputs = tokenizer('Привет, как дела?', return_tensors='pt')

# Generate a response using the model
generated_token_ids = model.generate(
    inputs['input_ids'],
    max_length=50,
    num_beams=5,
    no_repeat_ngram_size=2,
    early_stopping=True
)

# Decode the generated tokens to a readable text
response = tokenizer.decode(generated_token_ids[0], skip_special_tokens=True)

print(response)
