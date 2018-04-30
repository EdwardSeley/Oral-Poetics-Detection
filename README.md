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

## Detecting Rhymes
This script is built on top of Gentle, and thus uses Gentle's forced aligner to match each word with it's phonetic pronunciation. For example, the first seven lines of the Night Before Christmas in written English:

> Twas the night before Christmas, when all through the house
> Not a creature was stirring, not even a mouse;
> The stockings were hung by the chimney with care,
> In hopes that St. Nicholas soon would be there;
> The children were nestled all snug in their beds;
> While visions of sugar-plums danced in their heads;
> And mamma in her 'kerchief, and I in my cap,
> Had just settled our brains for a long winter's nap.

Once fed to the poetic detection script (which sends it to the forced aligner), these lines become:

```
['oov', 'dhah', 'nayt', 'bihfaor', 'krihsmahs', 'wehn', 'aol', 'thruw', 'dhiy', 'hhaws', 'naat', 'ah', 'kriycher', 'wahz', 'sterihng', 'naat', 'ah', 'maws', 'dhah', 'staakihngz', 'wer', 'hhahng', 'bay', 'dhah', 'chihmniy', 'wihth', 'kehr', 'ihn', 'hhowps', 'dhaht', 'seynt', 'nihkahlahs', 'suwn', 'wuhd', 'biy', 'dhehr', 'dhah', 'chihldrahn', 'wer', 'nehsahld', 'aol', 'snahg', 'ihn', 'dhehr', 'behdz', 'wayl', 'vihzhahnz', 'ahv', 'shuhger', 'plahmz', 'daenst', 'ihn', 'dhehr', 'hhehdz', 'ahnd', 'maamah', 'ihn', 'hher', 'oov', 'aend', 'ay', 'ihn', 'may', 'kaep', 'hhaed', 'jhihst', 'sehtahld', 'aar', 'breynz', 'fer', 'ah', 'laong', 'wihnterz', 'naep']
```
The rhyme detection algorithm works by finding the last syllable of each word and then comparing all of them by similarity and proximity (and filtering out stop words such as 'the' and 'a') in order to find rhymes. The last syllables are found simply by taking the last vowel/diphthong and all of the proceeding consonants. Using these methods, the following rhymes were detected:

```
[(('mouse', 'maws'), ('house', 'hhaws')), 
(('heads', 'hhehdz'), ('beds', 'behdz')), 
(('nap', 'naep'), ('cap', 'kaep'))]
```

## Detecting Alliterations
The algorithm for finding alliterations is very similar to that for finding rhymes. But instead of comparing the last syllable of nearby words, we are finding the first phone of each word that is in a very close proximity. Just as before, the first step is getting the phones for each spoken word in the text. I'll be using a verse from The Rime of the Ancient Mariner for this example:

> The western wave was all a flame.
> The day was well nigh done!
> Almost upon the western wave
> Rested the broad bright Sun;
> When that strange shape drove suddenly
> Betwixt us and the Sun. 

After these lines (and the accompanying audio) are given to the script, the following phones are gathered:

```
['dhah', 'wehstern', 'weyv', 'wahz', 'aol', 'ah', 'fleym', 'dhah', 'dey', 'wahz', 'wehl', 'nay', 'dahn', 'aolmowst', 'ahpaan', 'dhah', 'wehstern', 'weyv', 'rehstihd', 'dhah', 'braod', 'brayt', 'sahn', 'wehn', 'dhaet', 'streynjh', 'sheyp', 'drowv', 'sahdahnliy', 'oov', 'ahs', 'ahnd', 'dhah', 'sahn']
```

The first phone is then pulled from each word and compared to all of first phones of words nearby (3 words apart). All of these combinations are then brought together into a set of shared alliterations and added to the list:

```
[(('was', 'wahz'), ('well', 'wehl'), ('wave', 'weyv'), ('western', 'wehstern')), (('bright', 'brayt'), ('broad', 'braod')), (('us', 'ahs'), ('and', 'ahnd'))]

```

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
