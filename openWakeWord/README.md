![Github CI](https://github.com/dscripka/openWakeWord/actions/workflows/tests.yml/badge.svg)

# openWakeWord

openWakeWord is an open-source wakeword library that can be used to create voice-enabled applications and interfaces. It includes pre-trained models for common words & phrases that work well in real-world environments.

**Quick Links**
- [Installation](#installation)
- [Training New Models](#training-new-models)
- [FAQ](#faq)

# Updates

**2023/10/11**
- Significant improvements to the process of [training new models](#training-new-models), including an example Google Colab notebook demonstrating how to train a basic wake word model in <1 hour.

**2023/06/15**
- v0.5.0 of openWakeWord released. See the [changelog](CHANGELOG.md) for a full descriptions of new features and changes.

# Demo

You can try an online demo of the included pre-trained models via HuggingFace Spaces [right here](https://huggingface.co/spaces/davidscripka/openWakeWord)!

Note that real-time detection of a microphone stream can occasionally behave strangely in Spaces. For the most reliable testing, perform a local installation as described below.

# Installation

Installing openWakeWord is simple and has minimal dependencies:

```
pip install openwakeword
```

On Linux systems, both the [onnxruntime](https://pypi.org/project/onnxruntime/) package and [tflite-runtime](https://pypi.org/project/tflite-runtime/) packages will be installed as dependencies since both inference frameworks are supported. On Windows, only onnxruntime is installed due to a lack of support for modern versions of tflite.

To (optionally) use [Speex](https://www.speex.org/) noise suppression on Linux systems to improve performance in noisy environments, install the Speex dependencies and then the pre-built Python package (see the assets [here](https://github.com/dscripka/openWakeWord/releases/tag/v0.1.1) for all .whl versions), adjusting for your python version and system architecture as needed.

```
sudo apt-get install libspeexdsp-dev
pip install https://github.com/dscripka/openWakeWord/releases/download/v0.1.1/speexdsp_ns-0.1.2-cp38-cp38-linux_x86_64.whl
```

Many thanks to [TeaPoly](https://github.com/TeaPoly/speexdsp-ns-python) for their Python wrapper of the Speex noise suppression libraries.

# Usage

For quick local testing, clone this repository and use the included [example script](examples/detect_from_microphone.py) to try streaming detection from a local microphone. You can individually download pre-trained models from current and past [releases](https://github.com/dscripka/openWakeWord/releases/), or you can download them using Python (see below).

Adding openWakeWord to your own Python code requires just a few lines:

```python
import openwakeword
from openwakeword.model import Model

# One-time download of all pre-trained models (or only select models)
openwakeword.utils.download_models()

# Instantiate the model(s)
model = Model(
    wakeword_models=["path/to/model.tflite"],  # can also leave this argument empty to load all of the included pre-trained models
)

# Get audio data containing 16-bit 16khz PCM audio data from a file, microphone, network stream, etc.
# For the best efficiency and latency, audio frames should be multiples of 80 ms, with longer frames
# increasing overall efficiency at the cost of detection latency
frame = my_function_to_get_audio_frame()

# Get predictions for the frame
prediction = model.predict(frame)
```

Additionally, openWakeWord provides other useful utility functions. For example:

```python
# Get predictions for individual WAV files (16-bit 16khz PCM)
from openwakeword.model import Model

model = Model()
model.predict_clip("path/to/wav/file")

# Get predictions for a large number of files using multiprocessing
from openwakeword.utils import bulk_predict

bulk_predict(
    file_paths = ["path/to/wav/file/1", "path/to/wav/file/2"],
    wakeword_models = ["hey jarvis"],
    ncpu=2
)
```

See `openwakeword/utils.py` and `openwakeword/model.py` for the full specification of class methods and utility functions.

# Recommendations for Usage

## Noise Suppression and Voice Activity Detection (VAD)

While the default settings for openWakeWord will work well in many cases, there are adjustable parameters in openWakeWord that can improve performance in some deployment scenarios.

On supported platforms (currently only X86 and Arm64 linux), Speex noise suppression can be enabled by setting the `enable_speex_noise_suppression=True` when instantiating an openWakeWord model. This can improve performance when relatively constant background noise is present.

Second, a voice activity detection (VAD) model from [Silero](https://github.com/snakers4/silero-vad) is included with openWakeWord, and can be enabled by setting the `vad_threshold` argument to a value between 0 and 1 when instantiating an openWakeWord model. This will only allow a positive prediction from openWakeWord when the VAD model simultaneously has a score above the specified threshold, which can significantly reduce false-positive activations in the present of non-speech noise.

## Threshold Scores for Activation

All of the included openWakeWord models were trained to work well with a default threshold of `0.5` for a positive prediction, but you are encouraged to determine the best threshold for your environment and use-case through testing. For certain deployments, using a lower or higher threshold in practice may result in significantly better performance.

## User-specific models

If the baseline performance of openWakeWord models is not sufficient for a given application (specifically, if the false activation rate is unacceptably high), it is possible to train [custom verifier models](docs/custom_verifier_models.md) for specific voices that act as a second-stage filter on predictions (i.e., only allow activations through that were likely spoken by a known set of voices). This can greatly improve performance, at the cost of making the openWakeWord system less likely to respond to new voices.

# Project Goals

openWakeWord has four high-level goals, which combine to (hopefully!) produce a framework that is simple to use *and* extend.

1) Be fast *enough* for real-world usage, while maintaining ease of use and development. For example, a single core of a Raspberry Pi 3 can run 15-20 openWakeWord models simultaneously in real-time. However, the models are likely still too large for less powerful systems or micro-controllers. Commercial options like [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/) or [Fluent Wakeword](https://fluent.ai/products/wakeword/) are likely better suited for highly constrained hardware environments.

2) Be accurate *enough* for real-world usage. The included models are typically have false-accept and false-reject rates below the annoyance threshold for the average user. This is obviously subjective, by a false-accept rate of <0.5 per hour and a false-reject rate of <5% is often reasonable in practice. See the [Performance & Evaluation](#performance-and-evaluation) section for details about how well the included models can be expected to perform in practice.

2) Have a simple model architecture and inference process. Models process a stream of audio data in 80 ms frames, and return a score between 0 and 1 for each frame indicating the confidence that a wake word/phrase has been detected. All models also have a shared feature extraction backbone, so that each additional model only has a small impact to overall system complexity and resource requirements.

4) Require **little to no manual data collection** to train new models. The included models (see the [Pre-trained Models](#pre-trained-models) section for more details) were all trained with *100% synthetic* speech generated from text-to-speech models. Training new models is a simple as generating new clips for the target wake word/phrase and training a small model on top of of the frozen shared feature extractor. See the [Training New Models](#training-new-models) section for more details.

Future releases of openWakeWord will aim to stay aligned with these goals, even when adding new functionality.

# Pre-Trained Models

openWakeWord comes with pre-trained models for common words & phrases. Currently, only English models are supported, but they should be reasonably robust across different types speaker accents and pronunciation.

The table below lists each model, examples of the word/phrases it is trained to recognize, and the associated documentation page for additional detail. Many of these models are trained on multiple variations of the same word/phrase; see the individual documentation pages for each model to see all supported word & phrase variations.

| Model | Detected Speech | Documentation Page |
| ------------- | ------------- | ------------- |
| alexa | "alexa"| [docs](docs/models/alexa.md) |
| hey mycroft | "hey mycroft" | [docs](docs/models/hey_mycroft.md) |
| hey jarvis | "hey jarvis" | [docs](docs/models/hey_jarvis.md) |
| hey rhasspy | "hey rhasspy" | TBD
| current weather | "what's the weather" | [docs](docs/models/weather.md) |
| timers | "set a 10 minute timer" | [docs](docs/models/timers.md) |

Based on the methods discussed in [performance testing](#performance-and-evaluation), each included model aims to meet the target performance criteria of <5% false-reject rates and <0.5/hour false-accept rates with appropriate threshold tuning. These levels are subjective, but hopefully are below the annoyance threshold where the average user becomes frustrated with a system that often misses intended activations and/or causes disruption by activating too frequently at undesired times. For example, at these performance levels a user could expect to have the model process continuous mixed content audio of several hours with at most a few false activations, and have a failed intended activation in only 1/20 attempts (and a failed retry in only 1/400 attempts). 

If you have a new wake word or phrase that you would like to see included in the next release, please open an issue, and we'll do a best to train a model! The focus of these requests and future release will be on words and phrases that have broad general usage versus highly specific application.

# Model Architecture

openWakeword models are composed of three separate components:

1) A pre-processing function that computes [melspectrogram](https://pytorch.org/audio/main/generated/torchaudio.transforms.MelSpectrogram.html) of the input audio data. For openWakeword, an ONNX implementation of Torch's melspectrogram function with fixed parameters is used to enable efficient performance across devices.

2) A shared feature extraction backbone model that converts melspectrogram inputs into general-purpose speech audio embeddings. This [model](https://arxiv.org/abs/2002.01322) is provided by [Google](https://tfhub.dev/google/speech_embedding/1) as a TFHub module under an [Apache-2.0](https://opensource.org/licenses/Apache-2.0) license. For openWakeWord, this model was manually re-implemented to separate out different functionality and allow for more control of architecture modifications compared to a TFHub module. The model itself is series of relatively simple convolutional blocks, and gains its strong performance from extensive pre-training on large amounts of data. This model is the core component of openWakeWord, and enables the strong performance that is seen even when training on fully-synthetic data.

3) A classification model that follows the shared (and frozen) feature extraction model. The structure of this classification model is arbitrary, but in practice a simple fully-connected network or 2 layer RNN works well.

# Performance and Evaluation

Evaluating wake word/phrase detection models is challenging, and it is often very difficult to assess how different models presented in papers or other projects will perform *when deployed* with respect to two critical metrics: false-reject rates and false-accept rates. For clarity in definitions:

A *false-reject* is when the model fails to detect an intended activation from a user.

A *false-accept* is when the model inadvertently activates when the user did not intend for it to do so.

For openWakeWord, evaluation follows two principles:

- The *false-reject* rate should be determined from wakeword/phrases that represent realistic recording environments, including those with background noise and reverberation. This can be accomplished by directly collected data from these environments, or simulating them with data augmentation methods.

- The *false-accept* rate should be determined from audio that represents the types of environments that would be expected for the deployed model, not just on the training/evaluation data. In practice, this means that the model should only rarely activate in error, even in the presence of hours of continuous speech and background noise.

While other wakeword evaluation standards [do exist](https://github.com/Picovoice/wake-word-benchmark), for openWakeWord it was decided that a custom evaluation would better indicate what performance users can expect for real-world deployments. Specifically:

1) *false-reject* rates are calculated from either clean recordings of the wakeword that are mixed with background noise at realistic signal-to-noise ratios (e.g., 5-10 dB) *and* reverberated with room Impulse Response Functions (RIRs) to better simulate far-field audio, *or* manually collected data from realistic deployment environments (e.g., far-field capture with normal environment noise).

2) *false-accept* rates are determined by using the [Dinner Party Corpus](https://www.amazon.science/publications/dipco-dinner-party-corpus) dataset, which represents ~5.5 hours of far-field speech, background music, and miscellaneous noise. This dataset sets a realistic (if challenging) goal for how many false activations might occur in a similar situation.

To illustrate how openWakeWord can produce capable models, the false-accept/false-reject curves for the included `"alexa"` model is shown below along with the performance of a strong commercial competitor, [Picovoice Porcupine](https://picovoice.ai/platform/porcupine/). Other existing open-source wakeword engines (e.g., [Snowboy](https://github.com/Kitt-AI/snowboy), [PocketSphinx](https://github.com/cmusphinx/pocketsphinx), etc.) are not included as they are either no longer maintained or demonstrate performance significantly below that of Porcupine. The positive test examples used were those included in [Picovoice's](https://github.com/Picovoice/wake-word-benchmark) repository, a fantastic resource that they have freely provided to the community. Note, however, that the test data was prepared differently compared to Picovoice's implementation (see the [Alexa model documentation](docs/models/alexa.md) for more details).

![FPR/FRR curve for "alexa" pre-trained model](docs/models/images/alexa_performance_plot.png)

For at least this test data and preparation, openWakeWord produces a model that is more accurate than Porcupine.

As a second illustration, the false-accept/false-reject rate of the included `"hey mycroft"` model is shown below along with the performance of a [custom](https://picovoice.ai/docs/quick-start/porcupine-python/#custom-keywords) Picovoice Porcupine model and [Mycroft Precise](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/precise). In this case, the positive test examples were manually collected from a male speaker with a relatively neutral American english accent in realistic home recording scenarios (see the [Hey Mycroft model documentation](docs/models/hey_mycroft.md) for more details).

![FPR/FRR curve for "hey mycroft" pre-trained model](docs/models/images/hey_mycroft_performance.png)

Again, for at least this test data and preparation, openWakeWord produces a model at least as good as existing solutions.

However, in should noted that for both of these tests sample sizes are small and there are issues ([1](https://github.com/Picovoice/wake-word-benchmark/issues/13), [2](https://github.com/MycroftAI/mycroft-precise/issues/237)) with the evaluation of the other libraries that suggest these results should be interpreted cautiously. As such, the only claim being made is that openWakeWord models are broadly competitive with comparable offerings. You are strongly encouraged to [test openWakeWord](#installation--usage) to determine if it will meet the requirements of your use-case.

Finally, to give evidence that the core methods behind openWakeWord (i.e., pre-trained speech embeddings and high-quality synthetic speech) are effective across a wider range of wake word/phrase structure and length, the table below shows the performance on the [Fluent Speech Commands](https://paperswithcode.com/sota/spoken-language-understanding-on-fluent) test set using an openWakeWord model and the baseline method shown in a [related paper by the dataset authors](https://arxiv.org/abs/1910.09463). While both models were trained on fully-synthetic data, due to fundamentally different data synthesis & preparation, training, and evaluation approaches, the numbers below are likely not directly comparable. Rather, the important conclusion is that openWakeWord is a viable approach for the task of spoken language understanding (SLU).

| Model | Test Set Accuracy | Link |
| ------------- | ------------- | ------------- |
| openWakeWord | ~97.5% | NA |
| encoder-decoder | ~94.9% | [paper](https://arxiv.org/abs/1910.09463) |


If you are aware of other open-source wakeword/phrase libraries that should be added to these comparisons, or have suggestions on how to improve the evaluation more generally, please open an issue! We are eager to continue improving openWakeWord by learning how others are approaching this problem.

## Other Performance Details

### Model Robustness

Due to a combination of variability in the generated speech and the extensive pre-training from Google, openWakeWord models also demonstrate some additional performance benefits that are useful for real-world applications. In testing, three in particular have been observed.

1) The trained models seem to respond reasonably well to wakewords and phrases that are [whispered](https://en.wikipedia.org/wiki/Whispering). This is somewhat surprising behavior, as the text-to-speech models used for producing training data generally do not create synthetic speech that has acoustic qualities similar to whispering.

2) The models also respond relatively well to wakewords and phrases spoken at different speeds (within reason).

3) The models are able to handle some variability in the phrasing of a given command. This behavior was not entirely a surprise, given that [others](https://arxiv.org/abs/1904.03670) have reported similar benefits when training end-to-end spoken language understanding systems. For example, the included [pre-trained weather model](docs/models/weather.md) will typically still respond correctly to a phrase like "how is the weather today" despite not training directly on that phrase (though false rejections rates will likely be higher, on average, compared to phrases closer to the training data).

### Background Noise

While the models are trained with background noise to increase robustness, in some cases additional noise suppression can improve performance. Setting the `enable_speex_noise_suppression=True` argument during openWakeWord model initialization will use the efficient Speex noise suppression algorithm to pre-process the audio data prior to prediction. This can reduce both false-reject rates and false-accept rates, though testing in a realistic deployment environment is strongly recommended.

# Training New Models

openWakeWord includes an automated utility that greatly simplifies the process of training custom models. This can be used in two ways:

1) A simple [Google Colab](https://colab.research.google.com/drive/1q1oe2zOyZp7UsB3jJiQ1IFn8z5YfjwEb?usp=sharing) notebook with an easy to use interface and simple end-to-end process. This allows anyone to produce a custom model very quickly (<1 hour) and doesn't require any development experience, but the performance of the model may be low in some deployment scenarios.

2) A more detailed [notebook](notebooks/automatic_model_training.ipynb) (also on [Google Colab](https://colab.research.google.com/drive/1yyFH-fpguX2BTAW8wSQxTrJnJTM-0QAd?usp=sharing)) that describes the training process in more details, and enables more customization. This can produce high quality models, but requires more development experience.

For users interested in understanding the fundamental concepts behind model training there is a more detailed, educational [tutorial notebook](notebooks/training_models.ipynb) also available. However, this specific notebook is not intended for training production models, and the automated process above is recommended for that purpose.

Fundamentally, a new model requires two data generation and collection steps:

1) Generate new training data for the desired wakeword/phrase using open-source speech-to-text systems (see [Synthetic Data Generation](docs/synthetic_data_generation.md) for more details). These models and the generation code are hosted in a separate [repository](https://github.com/dscripka/synthetic_speech_dataset_generation). The number of generated examples required can vary, a minimum of several thousand is recommended and performance seems to increase smoothly with increasing dataset size.

2) Collect negative data (e.g., audio where the wakeword/phrase is not present) to help the model have a low false-accept rate. This also benefits from scale, and the [included models](#pre-trained-models) were all trained with ~30,000 hours of negative data representing speech, noise, and music. See the individual model documentation pages for more details on training data curation and preparation.

# Language Support

Currently, openWakeWord only supports English, primarily because the pre-trained text-to-speech models used to generate training data are all based on english datasets. It's likely that speech-to-text models trained on other languages would also work well, but non-english models & datasets are less commonly available.

Future release road maps may have non-english support. In particular, [Mycroft.AIs Mimic 3](https://github.com/MycroftAI/mimic3-voices) TTS engine may work well to help extend some support to other languages.

# FAQ

**Is there a Docker implementation for openWakeWord?**
- While there isn't an official Docker implementation, [@dalehumby](https://github.com/dalehumby) [has created one](https://github.com/dalehumby/openWakeWord-rhasspy) that works very well!

**Can openWakeWord be run in a browser with javascript?**
- While the ONNX runtime [does support javascript](https://onnxruntime.ai/docs/get-started/with-javascript.html), much of the other functionality required for openWakeWord models would need to be ported. This is not currently on the roadmap, but please open an issue/start a discussion if this feature is of particular interest.

**Is there a C++ version of openWakeWord?**
- While the ONNX runtime [also has a C++ API](https://onnxruntime.ai/docs/get-started/with-cpp.html), there isn't an official C++ implementation of the full openWakeWord library. However, [@synesthesiam](https://github.com/synesthesiam) has created a [C++ version](https://github.com/rhasspy/openWakeWord-cpp) of openWakeWord with basic functionality implemented.

**Why are there three separate models instead of just one?**
- Separating the models was an intentional choice to provide flexibility and optimize the efficiency of the end-to-end prediction process. For example, with separate melspectrogram, embedding, and prediction models, each one can operate on different size inputs of audio to optimize overall latency and share computations between models. It certainly is possible to make a combined model with all of the steps integrated, though, if that was a requirement of a particular use case.

**I still get a large number of false activations when I use the pre-trained models, how can I reduce these?**
- First, review the [recommendations for usage](#recommendations-for-usage) and ensure that these options do not improve overall system accuracy. Second, experiment with [custom verifier models](#user-specific-models), if possible. If neither of these approaches are helping, please open an issue with details of the deployment environment and the types of false activations that you are experiencing. We certainly appreciate feedback & requests on how to improve the base pre-trained models!

# Acknowledgements

I am very grateful for the encouraging and positive response from the open-source community since the release of openWakeWord in January 2023. In particular, I want to acknowledge and thank the following individuals and groups for their feedback, collaboration, and development support:

- [synesthesiam](https://github.com/synesthesiam)
- [SecretSauceAI](https://github.com/secretsauceai)
- [OpenVoiceOS](https://github.com/OpenVoiceOS)
- [Nabu Casa](https://github.com/NabuCasa)
- [Home Assistant](https://github.com/home-assistant)

# License

All of the code in this repository is licensed under the **Apache 2.0** license. All of the included pre-trained models are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) license due to the inclusion of datasets with unknown or restrictive licensing as part of the training data. If you are interested in pre-trained models with more permissive licensing, please raise an issue and we will try to add them to a future release.
