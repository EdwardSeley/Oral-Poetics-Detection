import sys
import multiprocessing
import os
sys.path.insert(0, '/gentle')
sys.path.insert(0, '/gentle/gentle/util')
import gentle
import pickle
import numpy as np
import nltk
from nltk.corpus import stopwords
import itertools

VOWELS = ['ay', 'ao', 'ih', 'ah', 'eh', 'uw', 'aw', 'aa', 'ae', 'iy', 'er', 'aw', 'eh', 'ow', 'ey', 'uw', 'uh']

class Word:
    def __init__(self, word, phones):
        self.word = word
        self.phones = phones

'''
Finds all of the rhymes in a text by getting the last syllables of all the words and comparing their proximity
and filtering out stop words
'''
def get_rhymes(words):
    last_syllables = []
    for word in words:
        syllable = get_last_syllable(word)
        last_syllables.append(syllable)
    rhymes = []
    for sequence in matching_occurrences(last_syllables):
        for pair in list(itertools.combinations(sequence, 2)):
            if abs(pair[1] - pair[0]) < 15:
                if last_syllables[pair[1]] != 'oov':
                    if words[pair[0]].word.lower() not in set(stopwords.words('english')) and words[pair[1]].word.lower() not in set(stopwords.words('english')):
                        rhymes.append(pair)
    return rhymes

'''
Gets the last syllable of the word by finding the last vowel
and all succeeding consonants
'''
def get_last_syllable(word):
    last_syllable = ""
    for phone in word.phones:
        if phone in VOWELS:
            last_syllable = ""
        last_syllable += phone
    return last_syllable

'''
Finds all equivalent elements in a sequences and returns their matching_indices
'''
def matching_occurrences(sequence):
    index = 0
    total_matches = []
    previous_matches  = []
    for element in sequence:
        postSequence = sequence[index + 1:len(sequence)]
        matches = []
        removals = 0
        if element not in previous_matches:
            while element in postSequence:
                match = postSequence.index(element) + removals + index + 1
                matches.append(match)
                postSequence.remove(element)
                removals += 1
            if removals != 0:
                previous_matches.append(element)
                matches.append(index)
                total_matches.append(matches)
            removals = 0
        index += 1
    return total_matches

TRANSCRIPT_PATH = "/data/Night_Before_Christmas.txt"
AUDIO_PATH = "/data/Night_Before_Christmas.mp3"

with open(os.getcwd() + TRANSCRIPT_PATH) as file:
    transcript = file.read()

resources = gentle.Resources()

'''
with gentle.resampled(os.getcwd() + AUDIO_PATH) as wavfile:
    aligner = gentle.ForcedAligner(resources, transcript)
    result = aligner.transcribe(wavfile)


with open('transcription.pkl', 'wb') as output:
    transcribed_words = []
    for word in result.words:
        phones = word.phones
        print(word.word)
        if phones is not None:
            root_phones = []
            for phone in phones:
                root_phone = phone['phone'][0:phone['phone'].index('_')]
                root_phones.append(root_phone)
            transcribed_words.append(Word(word.word, root_phones))

    pickle.dump(transcribed_words, output, pickle.HIGHEST_PROTOCOL)
        #last_syllable =
        #phoneme_dict[]
'''

with open('transcription.pkl', 'rb') as input:
    transcribed_words = pickle.load(input)
    get_rhymes(transcribed_words)
