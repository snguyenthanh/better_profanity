# -*- coding: utf-8 -*-

from io import open
from itertools import product

from .utils import (ALLOWED_CHARACTERS, any_next_words_form_swear_word,
                    get_complete_path_of_file, get_next_words,
                    get_start_index_of_next_word, load_unicode_symbols)

## GLOBAL VARIABLES ##
CENSOR_WORDSET = set()
CHARS_MAPPING = {
    "a": ("a", "@", "*", "4"),
    "i": ("i", "*", "l", "1"),
    "o": ("o", "*", "0", "@"),
    "u": ("u", "*", "v"),
    "v": ("v", "*", "u"),
    "l": ("l", "1"),
    "e": ("e", "*", "3"),
    "s": ("s", "$", "5"),
}

# Compatibility with Python 2
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

# Pre-load the unicode characters
load_unicode_symbols()

# The max number of additional words forming a swear word. For example:
# - hand job = 1
# - this is a fish = 3
MAX_NUMBER_COMBINATIONS = 1


def count_non_allowed_characters(word):
    count = 0
    for char in iter(word):
        if char not in ALLOWED_CHARACTERS:
            count += 1
    return count


def load_censor_words(custom_words=None):
    """Generate a set of words that need to be censored."""
    global CENSOR_WORDSET
    global MAX_NUMBER_COMBINATIONS

    # Replace the words from `profanity_wordlist.txt` with a custom list
    if custom_words:
        temp_words = custom_words
    else:
        temp_words = read_wordlist()

    all_censor_words = set()
    for word in temp_words:
        # All words in CENSOR_WORDSET must be in lowercase
        word = word.lower()
        num_of_non_allowed_chars = count_non_allowed_characters(word)
        if num_of_non_allowed_chars > MAX_NUMBER_COMBINATIONS:
            MAX_NUMBER_COMBINATIONS = num_of_non_allowed_chars

        all_censor_words.update(set(generate_patterns_from_word(word)))

    # The default wordlist takes ~5MB+ of memory
    CENSOR_WORDSET = all_censor_words

def add_censor_words(custom_words):
    global CENSOR_WORDSET

    if not isinstance(custom_words, (list, tuple, set)):
        raise TypeError("Function 'add_censor_words' only accepts list, tuple or set.")
    CENSOR_WORDSET.update(custom_words)


def generate_patterns_from_word(word):
    """Return all patterns can be generated from the word."""
    combos = [
        (char,) if char not in CHARS_MAPPING else CHARS_MAPPING[char]
        for char in iter(word)
    ]
    return ("".join(pattern) for pattern in product(*combos))


def read_wordlist():
    """Return words from file `profanity_wordlist.txt`."""
    wordlist_filename = "profanity_wordlist.txt"
    wordlist_path = get_complete_path_of_file(wordlist_filename)
    try:
        with open(wordlist_path, encoding="utf-8") as wordlist_file:
            for row in iter(wordlist_file):
                row = row.strip()
                if row != "":
                    yield row
    except FileNotFoundError:
        print("Unable to find profanity_wordlist.txt")


def get_replacement_for_swear_word(censor_char):
    return censor_char * 4


def contains_profanity(text):
    """Return True if  the input text has any swear words."""
    return text != censor(text)


def update_next_words_indices(text, words_indices, start_idx):
    """Return a list of next words_indices after the input index."""
    if not words_indices:
        words_indices = get_next_words(text, start_idx, MAX_NUMBER_COMBINATIONS)
    else:
        del words_indices[:2]
        if words_indices and words_indices[-1][0] != "":
            words_indices += get_next_words(text, words_indices[-1][1], 1)
    return words_indices


def hide_swear_words(text, censor_char):
    """Replace the swear words with censor characters."""
    censored_text = ""
    cur_word = ""
    skip_index = -1
    next_words_indices = []
    start_idx_of_next_word = get_start_index_of_next_word(text, 0)

    # If there are no words in the text, return the raw text without parsing
    if start_idx_of_next_word >= len(text) - 1:
        return text

    # Left strip the text, to avoid inaccurate parsing
    if start_idx_of_next_word > 0:
        censored_text = text[:start_idx_of_next_word]
        text = text[start_idx_of_next_word:]

    # Splitting each word in the text to compare with censored words
    for index, char in iter(enumerate(text)):
        if index < skip_index:
            continue
        if char in ALLOWED_CHARACTERS:
            cur_word += char
            continue

        # Skip continuous non-allowed characters
        if cur_word.strip() == "":
            censored_text += char
            cur_word = ""
            continue

        # Iterate the next words combined with the current one
        # to check if it forms a swear word
        next_words_indices = update_next_words_indices(text, next_words_indices, index)
        contains_swear_word, end_index = any_next_words_form_swear_word(
            cur_word, text, next_words_indices, CENSOR_WORDSET
        )
        if contains_swear_word:
            cur_word = get_replacement_for_swear_word(censor_char)
            skip_index = end_index
            char = ""
            next_words_indices = []

        # If the current a swear word
        if cur_word.lower() in CENSOR_WORDSET:
            cur_word = get_replacement_for_swear_word(censor_char)

        censored_text += cur_word + char
        cur_word = ""

    # Final check
    if cur_word != "" and skip_index < len(text) - 1:
        if cur_word.lower() in CENSOR_WORDSET:
            cur_word = get_replacement_for_swear_word(censor_char)
        censored_text += cur_word
    return censored_text


def censor(text, censor_char="*"):
    """Replace the swear words in the text with `censor_char`."""

    if not isinstance(text, str):
        text = str(text)
    if not isinstance(censor_char, str):
        censor_char = str(censor_char)

    if not CENSOR_WORDSET:
        load_censor_words()
    return hide_swear_words(text, censor_char)
