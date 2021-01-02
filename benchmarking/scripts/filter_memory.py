"""Measures how much memory a profanity filter consumes"""

import argparse
from memory_profiler import profile


@profile
def profile_default_wordlist():
    from better_profanity import profanity


@profile
def profile_custom_wordlist(wordlist_path):
    from better_profanity import Profanity

    Profanity(wordlist_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Profiles the memory usage of a better_profanity profanity filter"
    )
    parser.add_argument(
        "wordlist",
        nargs="?",
        type=str,
        default=None,
        help="word list containing profanity",
    )
    args = parser.parse_args()
    wordlist_path = args.wordlist

    # Profile the memory consumed by a filter using the default word list.
    profile_default_wordlist()

    # Profile the memory consumed by a filter using a custom word list.
    if wordlist_path is not None:
        profile_custom_wordlist(wordlist_path)
