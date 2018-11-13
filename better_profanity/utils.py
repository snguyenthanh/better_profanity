import json
import os.path
from string import ascii_letters, digits
from typing import List, Set, Tuple


## GLOBAL VARIABLES ##
ALLOWED_CHARACTERS = set(ascii_letters)
ALLOWED_CHARACTERS.update(set(digits))
ALLOWED_CHARACTERS.update({'@', '!', '$', '^', '*', '&', '\"', '\''})


def get_complete_path_of_file(filename: str) -> str:
    """Join the path of the current directory with the input filename."""
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, filename)


def load_unicode_symbols(unicode_symbols_json: str = "alphabetic_unicode.json"):
    with open(get_complete_path_of_file(unicode_symbols_json), "r") as json_file:
        ALLOWED_CHARACTERS.update(json.load(json_file))


def get_start_index_of_next_word(text: str, start_idx: int) -> int:
    start_idx_of_next_word = len(text)
    for index in iter(range(start_idx, len(text))):
        if text[index] not in ALLOWED_CHARACTERS:
            continue
        start_idx_of_next_word = index
        break

    return start_idx_of_next_word


def get_next_word_and_end_index(text: str, start_idx: int):
    next_word = ""
    index = start_idx
    for index in iter(range(start_idx, len(text))):
        char = text[index]
        if char in ALLOWED_CHARACTERS:
            next_word += char
            continue
        break
    return next_word, index


def any_next_words_form_swear_word(
    cur_word: str, text: str, words_indices: List[tuple], censor_words: Set[str]
):
    """Return True, and the end index of the word in the text, if any word formed in words_indices is in `CENSOR_WORDSET`."""
    full_word = cur_word.lower()
    full_word_with_separators = cur_word.lower()

    # Check both words in the pairs
    for index in iter(range(0, len(words_indices), 2)):
        single_word, end_index = words_indices[index]
        word_with_separators, _ = words_indices[index + 1]
        if single_word == "":
            continue

        full_word = "%s%s" % (full_word, single_word.lower())
        full_word_with_separators = "%s%s" % (full_word_with_separators, word_with_separators.lower())
        if full_word in censor_words or full_word_with_separators in censor_words:
            return True, end_index
    return False, -1

def get_next_words(text: str, start_idx: int, num_of_next_words: int = 1) -> List[Tuple[str, int]]:
    """
    Return a list of pairs of next words and next words included with separators, combined with their end indices.
    For example: Word `hand_job` has next words pairs: `job`, `_job`.
    """
    
    # Find the starting index of the next word
    start_idx_of_next_word = get_start_index_of_next_word(text, start_idx)

    # Return an empty string if there are no other words
    if start_idx_of_next_word >= len(text) - 1:
        return [("", start_idx_of_next_word), ("", start_idx_of_next_word)]

    # Combine the  words into a list
    next_word, end_index = get_next_word_and_end_index(text, start_idx_of_next_word)

    words = [
        (next_word, end_index),
        ("%s%s" % (text[start_idx:start_idx_of_next_word], next_word), end_index)
    ]
    if num_of_next_words > 1:
        words.extend(get_next_words(text, end_index, num_of_next_words - 1))

    return words
