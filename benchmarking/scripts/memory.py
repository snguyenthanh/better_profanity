"""Shows how much memory a Python process with a loaded Profanity filter takes up"""

import argparse
import os
import psutil


UNITS = ["B", "KB", "MB", "GB"]


def get_proc_bytes():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def human_readable(num_bytes):
    """
    Converts bytes to a human readable unit.

    Args:
        num_bytes: Bytes measurement to convert.

    Returns:
        str: The quantity with the unit symbol included.
    """
    num = num_bytes
    unit_sym = None
    for unit in UNITS[:-1]:
        if num < 1000:
            unit_sym = unit
            break
        else:
            num /= 1000
    unit_sym = unit_sym is None and UNITS[-1] or unit_sym
    if unit_sym == "B":
        return "{} {}".format(int(num), unit_sym)
    else:
        return "{:0.3f} {}".format(num, unit_sym)


def print_profile(msg, before=0):
    """
    Profiles the process' memory usage at this instant.

    Args:
        msg (str): Message/header to print before memory info.
        before (int): Amount of memory usage (in bytes) before the last operations.

    Returns:
        int: Total memory usage in bytes.
    """
    memory = get_proc_bytes()
    total = memory
    diff = memory - before
    print("  {}:".format(msg))
    print("    Total      : {} ({} B)".format(human_readable(total), total))
    print("    Difference : {} ({} B)".format(human_readable(diff), diff))
    return memory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Profiles the memory usage of better_profanity"
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

    print("Memory usage:")
    mem_baseline = print_profile("Baseline")

    from better_profanity import profanity, Profanity
    from better_profanity import __version__ as bp_version

    mem_after_import = print_profile(
        "After importing better_profanity (version {})".format(bp_version),
        mem_baseline,
    )

    if wordlist_path is not None:
        Profanity(wordlist_path)
        mem_after_wordlist = print_profile("After loading wordlist", mem_after_import)
