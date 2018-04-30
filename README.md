# Oral Poetics Detection
Using both Kaldi (Automatic Speech Recognition) and Gentle (Forced Word Aligner), the words of a spoken poem are matched with audio and used to find poetic devices such as alliteration and rhyme. This is made possible because Gentle's force aligner returns not only the times at which each word is spoken but also the phonetic pronunciation of each word. These phones are then able to be used to find patterns of oral speech in media files, such as the oration of the Night Before Christmas (uploaded as an example in the repository). 

## Install 
```
This repository is dependent on both [Kaldi](https://github.com/kaldi-asr/kaldi) and [Gentle](https://github.com/lowerquality/gentle).  
```

## Command Line Interface
```
python poetic_detection.py -h
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

## Getting a Phonetic Pronunciation
In order to align the words in a media file and obtain a pronunciation of them, both an audio file and transcript must be supplied.
