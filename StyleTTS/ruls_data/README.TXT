GENERAL INFORMATION
===================

Russian LibriSpeech (RuLS) dataset is based on LibriVox's public domain audio books (see BOOKS.TXT for the list of included books)
and contains about 98 hours of audio data.

The dataset was created by NVIDIA CORPORATION, 2020.
Contact info: ebakhturina@nvidia.com


The Russian LibriSpeech (RuLS) dataset is Public Domain in the USA. 


DIRECTORY STRUCTURE
===================

.
├── BOOKS.TXT                                            # Info about the books included in the corpus
├── CHAPTERS_READERS.TXT                                 # Info readers and corresponding chapters/books
├── dev                                                  # DEV (validation) subset
│   └── audio
│       └── 5397                                         # LibriVox READER ID
│             ├── 2145                                   # LibriVox BOOK ID                         
│                   ├── poemi_12_pushkin_0000.wav        # Audio file in .wav format, 16 kHz
│                   ├── poemi_12_pushkin_0001.wav   
│                   ├── ...
│   ├── manifest.json                                    # Manifest file 
│
│
├── README.TXT                                           # README file
│
├── test                                                 # TEST subset
│   └── audio
│       └── 2671                                         # LibriVox READER ID
│             ├── 2145                                   # LibriVox BOOK ID                         
│                   ├── poemi_01_pushkin_0000.wav        # Audio file in .wav format, 16 kHz
│                   ├── poemi_01_pushkin_0001.wav   
│                   ├── ...
│       └── ...             
│   ├── manifest.json                                    # Manifest file 
│
└── train                                                # TRAIN subset
    └── audio
        └── 13587                                        # LibriVox READER ID
              ├── 15349                                  # LibriVox BOOK ID                         
                    ├── vekhi_01_various_0000.wav        # Audio file in .wav format, 16 kHz  
                    ├── ...
        └── ...             
    ├── manifest.json                                    # Manifest file 



MANIFEST FILES
==============

Manifest files contain: 
  - audio_filepath: path to the audio file, 
  - duration: audio file duration, 
  - text: pre-processed text (text lowercased, punctuation removed),
  - text_no_preprocessing: original text, 
  - score: alignment score in log space (for more details see https://arxiv.org/abs/2007.09127)


REFERENCES
==========

Original LibriVox audio files were split into short segments using the CTC Segmentation project by Ludwig Kuerzinger et al.:  CTC-Segmentation of Large Corpora for German End-to-end Speech Recognition https://arxiv.org/abs/2007.09127.

@InProceedings{ctcsegmentation,
author="K{\"u}rzinger, Ludwig and Winkelbauer, Dominik and Li, Lujun and Watzel, Tobias and Rigoll, Gerhard",
editor="Karpov, Alexey and Potapova, Rodmonga",
title="CTC-Segmentation of Large Corpora for German End-to-End Speech Recognition", booktitle="Speech and Computer", year="2020",
publisher="Springer International Publishing", address="Cham", pages="267--278",
abstract="Recent end-to-end Automatic Speech Recognition (ASR) systems demonstrated the ability to outperform conventional hybrid DNN/HMM ASR. Aside from architectural improvements in those systems, those models grew in terms of depth, parameters and model capacity. However, these models also require more training data to achieve comparable performance.",
isbn="978-3-030-60276-5"
}
