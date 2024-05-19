# Emotional Offline Voice Assistant

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Emotional Offline Voice Assistant is an AI-driven voice assistant capable of understanding and expressing emotions. It can interact with users in a more human-like manner, providing a more engaging and natural user experience. This project is designed to work offline, ensuring user privacy and data security.

## Features

* Offline voice recognition and processing for enhanced privacy
* Emotion recognition and expression capabilities
* Natural language understanding for improved user interactions
* Customizable voice and personality
* Cross-platform compatibility

## Installation

To install the Emotional Offline Voice Assistant, follow these steps:

1. Clone the repository:

   Now clone this repository and dowload the pretrained speech model.
```bash
   git clone https://github.com/TPODAvia/Voice-Assistant
   cd Voice-Assistant
   curl -LJO "https://github.com/TPODAvia/Voice-Assistant/releases/download/v0.0.1-alpha/StyleTTS.zip"
   unzip StyleTTS.zip
   cd ../..
```

   Get the Microsoft Visual Studio:
```bash
   cd Voice-Assistant
   python -m venv venv
```
   if strugles of creating venv theen execute this code:

```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   python -m venv venv
   # or
   C:\Users\vboxuser\AppData\Local\Programs\Python\Python311\python.exe -m venv venv

```

Activate the venv

```bash
   ./venv/Script/activate
   # or
   .\venv\Scripts\activate
   # or
   ./venv/Scripts/Activate.ps1
```


2. Install the required dependencies:

Install torch with cuda
https://pytorch.org/get-started/locally/
To test that the cuda is working:
```bash
# activate your venv first
cd Voice-Assistant
python docs/cuda_test.py
```

Install espeak-NG
For Windows:

Download and install espeak-ng
https://github.com/espeak-ng/espeak-ng

Add to the system variables:
```bash
PHONEMIZER_ESPEAK_LIBRARY = C:\Program Files\eSpeak NG\libespeak-ng.dll
PHONEMIZER_ESPEAK_PATH = C:\Program Files\eSpeak NG
```

For Linux:

```bash
   sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python3-tk python3-dev sox python3-pil python3-pil.imagetk espeak -y
```

Install pip dependencies
```bash
   cd Voice-Assistant
   pip install -r requirements.txt
```
```bash
   pip install PyAudio
#    pip install transformers==4.39.0 # new realeases get errors when switching to offline mode
#    pip install openwakeword
#    pip install SoundFile torchaudio munch torch pydub pyyaml librosa git+https://github.com/resemble-ai/monotonic_align.git
```

3. Configure the voice assistant settings as needed:

```bash
   cd /home/vboxuser/Voice-Assistant/Irene-Voice-Assistant/options/core.json
   sudo nano core.json
```

<!-- 4. Run icon execution:

   Still in the developmant...

   Install bash for window:
```bash
   wsl --install
   bash script.sh
``` -->
5. Optionaly, the online voice assistance can be executed in the `Voice_assistant_online` folder:

```bash
   cd Voice_assistant_online
   python voice_assistant_online.py
```

## Usage

To start the Emotional Offline Voice Assistant, run the following command:

```bash
cd Voice-Assistant/Irene-Voice-Assistant
python3 runva_neuralnet.py
```

Once the voice assistant is running, you can interact with it using your microphone or by providing text input.

## Perfomance check

To create a profiling image using `gprof2dot` from the provided script, follow these steps:

1. **Profile the Script with `cProfile`:**
   Modify the script to use the `cProfile` module to collect profiling data.

2. **Run the Script to Generate Profiling Data:**
   Execute the modified script to generate a `.prof` file containing the profiling data.

3. **Convert Profiling Data to a Dot File:**
   Use `gprof2dot` to convert the `.prof` file to a `.dot` file.

4. **Generate an Image from the Dot File:**
   Use Graphviz to convert the `.dot` file to an image format like PNG.

Here is the step-by-step process:

### Step 1: Modify the Script to Use `cProfile`

Add the `cProfile` module to your script to collect profiling data:

```python
import sys
import cProfile

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.dump_stats('profile_data.prof')
```

### Step 2: Run the Script

Run the modified script to generate the `profile_data.prof` file:

```sh
python your_script.py
```

Terminate the script with `Ctrl+C` after a few seconds to ensure profiling data is collected.

### Step 3: Convert Profiling Data to a Dot File

Use `gprof2dot` to convert the `.prof` file to a `.dot` file:

```sh
gprof2dot -f pstats profile_data.prof -o profile_data.dot
```

### Step 4: Generate an Image from the Dot File

Use Graphviz to convert the `.dot` file to an image format like PNG:

```sh
dot -Tpng profile_data.dot -o profile_data.png
```

After these steps, you will have a `profile_data.png` file that visually represents the profiling data of your script.


## Contributing

We welcome contributions to the Emotional Offline Voice Assistant project. If you're interested in contributing, please read our [contribution guidelines](./CONTRIBUTING.md) and [code of conduct](./CODE_OF_CONDUCT.md) before getting started.

## License

This project is licensed under the [MIT License](./LICENSE.md).
