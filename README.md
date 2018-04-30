# Oral Poetics Detection
Using both Kaldi (Automatic Speech Recognition) and Gentle (Forced Word Aligner), the words of a spoken poem are matched with audio and used to find poetic devices such as alliteration and rhyme. This is made possible because Gentle's force aligner returns not only the times at which each word is spoken but also the phonetic pronunciation of each word. These phones are then able to be used to find patterns of oral speech in media files, such as the oration of the Night Before Christmas (uploaded as an example in the repository). 

# Getting a Phonetic Pronunciation
In order to align the words in a media file and obtain a pronunciation of them, both an audio file and transcript must be supplied.
