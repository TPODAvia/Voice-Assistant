## Wake word
[Youtube Video For WakeWord](https://www.youtube.com/watch?v=ob0p7G2QoHA&list=PL5rWfvZIL-NpFXM9nFr15RmEEh4F4ePZW)

### scripts
For more details make sure to visit these files to look at script arguments and description

`AudioReaction/neuralnet/0_train.py` is used to train the model

`AudioReaction/neuralnet/1_optimize_graph.py` is used to create a production ready graph that can be used in `engine.py`

`AudioReaction/engine.py` is used to demo the wakeword model

`AudioReaction/scripts/0_collect_wakeword_audio.py` - used to collect wakeword and environment data

`AudioReaction/scripts/2_split_audio_into_chunks.py` - used to split audio into n second chunks

`AudioReaction/scripts/3_split_commonvoice.py` - if you download the common voice dataset, use this script to split it into n second chunks

`AudioReaction/scripts/5_create_wakeword_txt.py` - used to create the wakeword txt for training

### Steps to train and demo your wakeword model

For more details make sure to visit these files to look at script arguments and description

#### 0 create dataset
    1. create your own dataset or copy the the examples from  `./data_s`. For the `engine.py` to be fully functional make sure you have 26 folders for training. The training process can be N folders.

```bash
    cd VoiceAssistant/AudioReaction/scripts
    mkdir data
    cp -a /data_s/. /data/
```

#### 1 collect data
    1. environment and wakeword data can be collected using `python 0_collect_wakeword_audio.py`

```bash
    cd VoiceAssistant/AudioReaction/scripts
    cd data_s
    mkdir 30 31 32
    cd ..
    python 0_collect_wakeword_audio.py --sample_rate 8000 --seconds 2 --interactive --interactive_save_path ./data_s/32
```
    2. to avoid the imbalanced dataset problem, we can duplicate the wakeword clips with 
```bash
    python 1_replicate_audios.py --wakewords_dir data_s/32/ --copy_destination data_s/32/ --copy_number 100
```
    3. be sure to collect other speech data like common voice. split the data into n seconds chunk with `2_split_audio_into_chunks.py`. Remember to modyfy the `audio_file_name` and `save_path` for your computer enviroment.
```bash
       python 2_split_audio_into_chunks.py
```
    4. put data into two seperate directory named `0`, `1` so on. Use `5_create_wakeword_txt.py` to create train and test txt
```bash
       python .\5_create_wakeword_txt.py
```
    5. create a train and test json in this format...
```bash
        # make each sample is on a seperate line
        {"key": "/path/to/audio/sample.wav, "label": 0}
        {"key": "/path/to/audio/sample.wav, "label": 1}
```
```bash
        and the txt format looks like this:
        "folder_name"/"file_name".wav
        1/aslan_25_chunk_0.wav
        0/tavuk_21_chunk_1.wav
        ...
```

#### 2 train model
    1. use `train.py` to train model
```bash
        cd \Voice-Assistant\AudioReaction\neuralnet

        python 0_train.py
```
    2. after model training us `optimize_graph.py` to create an optimized pytorch model
```bash
        cd \Voice-Assistant\AudioReaction\neuralnet

        python 1_optimize_graph.py
```

#### 3 test
    1. test using the `engine.py` script:

```bash
        cd \Voice-Assistant\AudioReaction

        python engine.py
```

### data_s information

```bash
    0 - chicken
    1 - lion
    2 - monkey
    3 - cow
    4 - cat
    5 - dog
    6 - shep
    7 - frog
    8 - bird
```

### deep neural network architecture

```bash
LSTMWakeWord(
  (layernorm): LayerNorm((40,), eps=1e-05, elementwise_affine=True)
  (lstm): LSTM(40, 128, dropout=0.1)
  (classifier): Linear(in_features=128, out_features=8, bias=True) 
)
```