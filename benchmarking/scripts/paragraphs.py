"""Benchmarks how fast better_profanity censors large bodies of text"""

from better_profanity import profanity
from better_profanity import __version__ as bp_version
import logging
import os
import sys
from time import time


logger = logging.getLogger("better_profanity")
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(
    logging.Formatter(
        fmt="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(handler)


def benchmark(original, censored, trials=4):
    """
    Measures the speed of censoring with better_profanity.

    Args:
        original (str): Original text.
        censored (str): Censored version of `original`.
        trials (int): Number of trials to run.

    Returns:
        float, bool: Average runtime for the `censor` operation over all trials in seconds,
            and whether the censored text actually matches `censored`.
    """
    total_time = 0
    censor_success = True
    for n in range(trials):
        start = time()
        orig_censored = profanity.censor(original)
        total_time = time() - start
        if n == 1 and orig_censored != censored:
            censor_success = False
    return total_time / trials, total_time, censor_success


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "../data/paragraphs/")
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        sys.exit('"{}" is not a directory'.format(root))
    print("Paragraph benchmarks for version {}".format(bp_version))
    print("\nAverage runtimes:")
    total_time = 0
    total_avg_time = 0
    try:
        for subdir in sorted(os.listdir(root)):
            new_root = os.path.join(root, subdir)
            if not os.path.isdir(new_root):
                continue
            orig_path = os.path.join(new_root, "original.txt")
            censor_path = os.path.join(new_root, "censored.txt")
            if not os.path.isfile(orig_path):
                logger.warning('"{}" is not a file'.format(orig_path))
                continue
            if not os.path.isfile(censor_path):
                logger.warning('"{}" is not a file'.format(censor_path))
                continue

            with open(orig_path) as f:
                original = f.read()
            with open(censor_path) as f:
                censored = f.read()

            avg_time, trial_total_time, success = benchmark(original, censored)
            if not success:
                logger.warning("Censoring failed for {}".format(subdir))
            print("  {}: {:0.4f}s".format(subdir, avg_time))
            total_time += trial_total_time
            total_avg_time += avg_time
    except KeyboardInterrupt:
        pass
    print()
    print("Total runtime: {:0.4f}s".format(total_time))
    print("Total average runtime: {:0.4f}s".format(total_avg_time))
