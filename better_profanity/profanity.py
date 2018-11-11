from itertools import product
from typing import Set, List
from string import ascii_lowercase, digits
import os.path
import sys

## GLOBAL VARIABLES ##
CENSOR_WORDSET = set()
CHARS_MAPPING = {
    'a': ('a', '@', '*', '4', '&'),
    'i': ('i', '*', 'l', '!', '1'),
    'o': ('o', '*', '0', '@'),
    'u': ('u', '*', 'v'),
    'v': ('v', '*', 'u'),
    'l': ('l', '1'),
    'e': ('e', '*', '3'),
    's': ('s', '$'),
}

ALLOWED_CHARACTERS = set(ascii_lowercase)
ALLOWED_CHARACTERS.update(set(digits))
ALLOWED_CHARACTERS.update(
    set(['@', '!', '$', '^', '*', '&', '\"', '\''])
)

# The max number of additional words forming a swear word. For example:
# - hand job = 1
# - this is a fish = 3
MAX_NUMBER_COMBINATIONS = 1


def get_complete_path_of_file(filename: str) -> str:
    """Join the path of the current directory with the input filename."""
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, filename)

def load_censor_words(custom_words: List=[]):
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
        num_of_spaces = word.count(" ")
        if num_of_spaces > MAX_NUMBER_COMBINATIONS:
            MAX_NUMBER_COMBINATIONS = num_of_spaces

        all_censor_words.update(
            set(generate_patterns_from_word(word))
        )

    # The default wordlist takes ~5MB+ of memory
    CENSOR_WORDSET = all_censor_words

def generate_patterns_from_word(word: str) -> Set[str]:
    """Return all patterns can be generated from the word."""
    combos = [
        (char,) if char not in CHARS_MAPPING
        else CHARS_MAPPING[char]
        for char in iter(word)
    ]
    return (''.join(pattern) for pattern in product(*combos))

def read_wordlist() -> Set[str]:
    """Return words from file `profanity_wordlist.txt`."""

    wordlist_filename = 'profanity_wordlist.txt'
    wordlist_path = get_complete_path_of_file(wordlist_filename)
    try:
        with open(wordlist_path, encoding='utf-8') as wordlist_file:
            # All CENSOR_WORDSET must be in lowercase
            for row in iter(wordlist_file):
                row = row.strip()
                if row != "":
                    yield row
    except FileNotFoundError:
        print('Unable to find profanity_wordlist.txt')
        pass

def get_replacement_for_swear_word(censor_char: str) -> str:
    return censor_char * 4

def contains_profanity(text: str) -> bool:
    """Return True if  the input text has any swear words."""
    return text != censor(text)

def get_next_words(text:str, start_idx: int, num_of_next_words: int=1) -> str:
    # Find the starting index of the next word
    start_idx_of_next_word = len(text)
    for index in iter(range(start_idx, len(text))):
        if text[index] not in ALLOWED_CHARACTERS:
            continue
        start_idx_of_next_word = index
        break

    # Return an empty string if there are no other words
    if start_idx_of_next_word == len(text) - 1:
        return [("", start_idx_of_next_word)]

    cur_word = ""
    index = start_idx_of_next_word
    for index in iter(range(start_idx_of_next_word, len(text))):
        char = text[index].lower()
        if char in ALLOWED_CHARACTERS:
            cur_word += char
            continue
        break

    # Combine the following words into a list
    words =  [(cur_word, index)]
    if num_of_next_words > 1:
        words.extend(
             get_next_words(text, index, num_of_next_words - 1)
        )

    return words

def hide_swear_words(text: str, censor_char: str) -> str:
    """Replace the swear words with censor characters."""
    censored_text = ""
    cur_word = ""
    skip_index = -1
    skip_cur_char = False

    # Splitting each word in the text to compare with censored words
    for index, char in iter(enumerate(text)):
        if index <= skip_index:
            continue

        if char.lower() in ALLOWED_CHARACTERS:
            cur_word += char
            continue

        # Iterate the next words combined with the current one
        # to check if it forms a swear word
        next_words_indices = get_next_words(text, index+1, MAX_NUMBER_COMBINATIONS)
        full_next_word = cur_word.lower()
        for next_word, end_index in iter(next_words_indices):
            full_next_word = "%s %s" % (full_next_word, next_word.lower())
            if full_next_word in CENSOR_WORDSET:
                cur_word = get_replacement_for_swear_word(censor_char)
                skip_index = end_index
                char = ""
                break

        # If the current a swear word
        if cur_word.lower() in CENSOR_WORDSET:
            cur_word = get_replacement_for_swear_word(censor_char)

        censored_text += cur_word
        censored_text += char
        cur_word = ""

    if cur_word != "" and skip_index < len(text):
        if cur_word.lower() in CENSOR_WORDSET:
            cur_word = get_replacement_for_swear_word(censor_char)
        censored_text += cur_word
    return censored_text

def censor(text: str, censor_char: str='*') -> str:
    """Replace the swear words in the text with `censor_char`."""

    if not isinstance(text, str):
        text = str(text)
    if not isinstance(censor_char, str):
        censor_char = str(censor_char)

    if not CENSOR_WORDSET:
        load_censor_words()
    return hide_swear_words(text, censor_char)

if __name__ == "__main__":
    #bad_text = "That wh0re gave m3 a very good H4nd j0b, dude. You gotta check"
    bad_text = "Corki"
    censored_text = censor(bad_text)
    print(censored_text)
