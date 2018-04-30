# Oral Poetics Detection
Using both Kaldi (Automatic Speech Recognition) and Gentle (Forced Word Aligner), the words of a spoken poem are matched with audio and used to find poetic devices such as alliteration and rhyme. This is made possible because Gentle's force aligner returns not only the times at which each word is spoken but also the phonetic pronunciation of each word. These phones are then able to be used to find patterns of oral speech in media files, such as the oration of the Night Before Christmas (uploaded as an example in the repository). 

## Install 
This repository is dependent on both [Kaldi](https://github.com/kaldi-asr/kaldi) and [Gentle](https://github.com/lowerquality/gentle). Simple install the Gentle repository, which contains a script to install Kaldi, and then place this cloned repository into the Gentle folder.  

## Command Line Interface
```
usage: poetic_detection.py [-h] -a AUDIO -t TEXT [-r] [-al]

Get poetic devices, such as rhyme and alliteration, from a given audio file
and text file.

optional arguments:
  -h, --help            show this help message and exit
  -a AUDIO, --audio AUDIO
                        audio file of clearly spoken English with minimal
                        background noise
  -t TEXT, --text TEXT  transcript file of the spoken words used in the audio
                        file
  -r, --rhyme           Retrieves all of the rhyming pairs found in the audio
                        and transcript files
  -al, --alliteration   Retrieves all of cases of alliteration found in the
                        audio and transcript files
```

## Usage
In order to align the words in a media file and obtain a pronunciation of them, both an audio file and transcript must be supplied. Throughout the README, I will be using Clement Moore's Night Before Christmas (A visit from St. Nicholas) as an example and both the accompanying text file and audio file can be found in the data folder of this repository. However, any audio file with clearly spoken and matching text can be used (American accents tend to work better than British and others).
