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
import argparse
import subprocess
import json

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
                    if words[pair[0]].word.lower() != words[pair[1]].word.lower():
                        if words[pair[0]].word.lower() not in set(stopwords.words('english')) and words[pair[1]].word.lower() not in set(stopwords.words('english')):
                            rhymes.append( ( (words[pair[0]].word, ''.join(words[pair[0]].phones)), (words[pair[1]].word, ''.join(words[pair[1]].phones))) )
    return rhymes

'''
In a very similar manner as to how rhymes were collected, the first phone of
each word was extracted and compared to each other based on proximity.
'''
def get_alliterations(words):
    first_phones = []
    for word in words:
        phone = get_first_phone(word)
        first_phones.append(phone)
    alliterations = []
    for sequence in matching_occurrences(first_phones):
        for pair in list(itertools.combinations(sequence, 2)):
            if abs(pair[1] - pair[0]) < 3:
                if first_phones[pair[1]] != 'oov':
                    alliterations.append( ( (words[pair[0]].word, ''.join(words[pair[0]].phones)), (words[pair[1]].word, ''.join(words[pair[1]].phones))) )

    return pairs_to_tuples(alliterations)

'''
From the list of tuple pairs, a set is created and the intersections of all the
pairs are gathered and placed into a more flexible tuple
'''
def pairs_to_tuples(sequence):
    set_of_sets = set([frozenset(element) for element in sequence])
    result = []
    while(set_of_sets):
        new_set = set(set_of_sets.pop())
        check = len(set_of_sets)
        while check:
            check = False
            for element in set_of_sets.copy():
                if new_set.intersection(element):
                    check = True
                    set_of_sets.remove(element)
                    new_set.update(element)
        result.append(tuple(new_set))
    return result

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
Simply returns the first phone of the word given
'''
def get_first_phone(word):
    return word.phones[0]

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

'''
Returns a list of all the words (belong to the Word class above) spoken in media files
'''
def get_transcribed_words(textFile, audioFile):
    with open(textFile) as file:
        transcript = file.read()

    resources = gentle.Resources()

    with gentle.resampled(audioFile) as wavfile:
        aligner = gentle.ForcedAligner(resources, transcript)
        result = aligner.transcribe(wavfile)

    transcribed_words = []
    for word in result.words:
        phones = word.phones
        if phones is not None:
            root_phones = []
            for phone in phones:
                root_phone = phone['phone'][0:phone['phone'].index('_')]
                root_phones.append(root_phone)
            transcribed_words.append(Word(word.word, root_phones))

    return transcribed_words

def main():

    parser = argparse.ArgumentParser(
            description='Get poetic devices, such as rhyme and alliteration, from a given audio file and text file.')

    parser.add_argument(
            '-a',
            '--audio',
            type=str,
            help='audio file of clearly spoken English with minimal background noise',
            required=True)

    parser.add_argument(
            '-t',
            '--text',
            type=str,
            help='transcript file of the spoken words used in the audio file',
            required=True)

    parser.add_argument(
            '-o',
            '--output',
            type=str,
            help='Stores the results of the poetic device detection in a JSON file',
            )

    args = parser.parse_args()

    transcribed_words = get_transcribed_words(args.text, args.audio)


    devices = {}
    devices["Rhymes"] = get_rhymes(transcribed_words)
    devices["Alliteration"] = get_alliterations(transcribed_words)
    print(devices)

    if args.output:
        js = json.dumps(devices)
        output_file = open(args.output, 'w')
        output_file.write(js)
        output_file.close()

if __name__ == '__main__':
    main()
