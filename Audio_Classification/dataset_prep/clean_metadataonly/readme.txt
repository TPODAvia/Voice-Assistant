freefield1010
=============

A dataset of standardised 10-second excerpts from Freesound field recordings.

Curated July 2013 by Dan Stowell at the Centre for Digital Music, QMUL, London.
Based on recordings from the Freesound archive <http://freesound.org/> hosted by the Music Technology Group, UPF, Barcelona.

Version 1.0


ABOUT
-----

This dataset contains 7690 10-second audio files in a standardised format, extracted from contributions on the Freesound archive which were labelled with the "field-recording" tag. Note that the original tagging (as well as the audio submission) is crowdsourced, so the dataset is not guaranteed to consist purely of "field recordings" as might be defined by practitioners. The intention is to represent the content of an archive collection on such a topic, rather than to represent a controlled definition of such a topic.

Each audio file has a corresponding text file, containing metadata such as author and tags. 
The dataset has been randomly split into 10 equal-size subsets. This is so that you can perform 10-fold crossvalidation in machine-learning experiments, or can use fixed subsets of the data (e.g. use one subset for development, and others for later validation). Each of the 10 subsets has about 128 minutes of audio; the dataset totals over 21 hours of audio.


COPYRIGHTS AND LICENSING
------------------------

Collection: (c) 2013 Dan Stowell and Queen Mary University London.
  This collection is published under the terms of the Creative Commons Attribution licence, version 3.0:
  http://creativecommons.org/licenses/by/3.0/

Audio files: Each file is (c) the Freesound user who uploaded the original file to Freesound. For author and licence information please see the JSON metadata file included with each audio file.

The audio files were selected (as described below) so that all content in the collection would be compatible with the CC-BY licence used for the collection overall.


FILE FORMATS AND LAYOUT
-----------------------

The dataset is partitioned into 10 subsets with an equal number of audio files in each. You may have these as zipfiles or as folders, named 01 02 03 04 05 06 07 08 09 10.

Each .wav file contained within has a numeric ID as a filename, which corresponds to the ID of the original audio file held in the Freesound archive. Note that the .wav file is NOT the same as the one on Freesound - it has been excerpted and standardised. Each .wav file is 10 seconds long, WAV, mono, sample rate 44.1 kHz, 16-bit PCM, amplitude normalised. The numeric ID used for filenames does not have a fixed number of digits but is as many as 6-digit.

Each .wav file also has a corresponding .json file, which is simply the metadata reported by the Freesound server while fetching the original audio. Notable keys are:

 * user:    the username and url for the Freesound user who uploaded this particular audio file. The copyright in the audio file remains with them.
 * license: the license of the audio file.
 * tags:    the list of tags associated with the file. "field-recording" will be but one.
 * id:      the Freesound ID - should match filename.
 * url:     a URL that takes you to the Freesound item page.
 * geotag:  a lat/lon pair indicating geolocation. Roughly one-third of the files include this tag - availability of geotag was not a criterion for constructing the dataset.

The JSON data includes fields such as "channels", "duration", "samplerate" - these refer to the original audio contribution, and not to the excerpt included here.

We also provide a file metadataonly.zip, which contains copies of the .json files. This zip contains no additional material - it is provided for convenience.


HOW THE DATASET WAS PREPARED
----------------------------

The files were downloaded from Freesound using a Python script "tagsearch.py", available in the following derived branch of the freesound-python code:
https://github.com/danstowell/freesound-python/tree/tagsearch

PLEASE NOTE: do not perform large bulk downloads from Freesound. We obtained specific permission before running this script.

The script was run to download all files matching all of the following criteria:

 * Tagged "field-recording"
 * Length 10 seconds or greater
 * Audio file format WAV
 * Content licensed under any one of the following licences:
         - http://creativecommons.org/licenses/by/3.0/
         - http://creativecommons.org/publicdomain/zero/1.0/
 * Audio with 1 or 2 channels
 * Audio sample format one of: pcm16, pcm24, pcm32

Each file was saved along with its metadata in JSON format.

A small number of files failed to download completely; these were detected by using the "sox" command to attempt WAV decoding, and deleting the files which reported EOF errors or similar.

We then prepared a 10-second standardised excerpt from each audio file, using the script "snippetmaker.py" available from the same location. This extracted a 10-second clip from the *middle* of the audio recording, and converted it to the standardised file format described above. Maximum gain was normalised to -2 dB for each file, empirically selected as the maximum gain before clipping. Audio conversion was done using "sox" command-line audio tool, v 14.3.2.

We inspected the excerpts, and found a few (7) which were pure silence with DC offset. While this may be valid audio when considered in context, it led to normalisation issues, and could be problematic for some applications; we decided to remove these files and re-run snippetmaker.

The snippetmaker script also placed the exerpts (along with their JSON metadata files) into the 10 separate partitions. Allocation of items to folds was done by pseudorandom shuffle initialised with a fixed seed value for repeatability (see Python script).

