# Emotional Offline Voice Assistant

![GitHub Repo stars](https://img.shields.io/github/stars/your-github-username/emotional-offline-voice-assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-github-username/emotional-offline-voice-assistant?style=social)
![GitHub Profile Views](https://komarev.com/ghpvc/?username=your-github-username&style=flat-square&color=blue)

<div align="center">
  <img src="https://media.giphy.com/media/dWesBcTLavkZuG35MI/giphy.gif" width="447" height="358"/>
</div>

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

   ```
   git clone https://github.com/TPODAvia/Voice-Assistant
   ```

2. Install the required dependencies:

   ```
   cd Voice-Assistant
   pip install -r requirements.txt
   sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 -y
   sudo apt-get install python3-tk python3-dev -y
   sudo pip install pyaudio
   ```

3. Configure the voice assistant settings as needed:

   ```
   cd /home/vboxuser/Voice-Assistant/Irene-Voice-Assistant/options/core.json
   sudo nano core.json
   ```

## Usage

To start the Emotional Offline Voice Assistant, run the following command:

```
cd Voice-Assistant/Irene-Voice-Assistant
python3 runva_neuralnet.py
```

Once the voice assistant is running, you can interact with it using your microphone or by providing text input.

## Contributing

We welcome contributions to the Emotional Offline Voice Assistant project. If you're interested in contributing, please read our [contribution guidelines](./CONTRIBUTING.md) and [code of conduct](./CODE_OF_CONDUCT.md) before getting started.

## License

This project is licensed under the [MIT License](./LICENSE.md).