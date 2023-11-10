# Emotional Offline Voice Assistant

https://machine-listening.eecs.qmul.ac.uk/bird-audio-detection-challenge/
https://drive.google.com/drive/folders/1KI7uF_-IYh3w4z0uLBNcCo3tRd-1nlm9?usp=sharing

![GitHub Repo stars](https://img.shields.io/github/stars/your-github-username/emotional-offline-voice-assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-github-username/emotional-offline-voice-assistant?style=social)
![GitHub Profile Views](https://komarev.com/ghpvc/?username=your-github-username&style=flat-square&color=blue)

<div align="center">
  <img src="https://media.giphy.com/media/dWesBcTLavkZuG35MI/giphy.gif" width="447" height="358"/>
</div>

## TODO:

- Replace the absolute path to relative path
- Update the ReadMe workflow (DONE)
- Modify the AudioReaction to the n class classification (DONE)
- Modyfy the UI and fix the UI bugs (DONE)
- Add the classification to the main runner (DONE)
- Write the paper for this project


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

```bash
   get the Microsoft Visual Studio

   python -m venv venv
```
   if strugles of creating venv theen execute this code:

```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

   python -m venv venv

   # or

   C:\Users\vboxuser\AppData\Local\Programs\Python\Python311\python.exe -m venv venv

```

   Now clone this repository
```
   git clone https://github.com/TPODAvia/Voice-Assistant
```

2. Install the required dependencies:

```bash
   cd Voice-Assistant
   pip install -r requirements.txt
   sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 python3-tk python3-dev sox python3-pil python3-pil.imagetk espeak -y
```
```bash
   pip install PyAudio
```

3. Configure the voice assistant settings as needed:

```bash
   cd /home/vboxuser/Voice-Assistant/Irene-Voice-Assistant/options/core.json
   sudo nano core.json
```

4. Run icon execution:

   Still in the developmant...

   Install bash for window:
```bash
   wsl --install
   bash script.sh
```
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

## Contributing

We welcome contributions to the Emotional Offline Voice Assistant project. If you're interested in contributing, please read our [contribution guidelines](./CONTRIBUTING.md) and [code of conduct](./CODE_OF_CONDUCT.md) before getting started.

## License

This project is licensed under the [MIT License](./LICENSE.md).