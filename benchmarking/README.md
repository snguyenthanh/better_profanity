# Benchmarking `better_profanity`

This directory provides code for benchmarking the memory usage and speed of `better_profanity`.

## Setup

Follow the **Installation** instructions for `better_profanity` to ensure the version you intend to benchmark is installed.

Install additional dependencies by running

```
pip install -r requirements.txt
```

## Usage

### Benchmark memory usage

To test the memory usage of a profanity filter using the default word list run

```
python scripts/filter_memory.py
```

To test the memory usage when using a particular word list run

```
python scripts/filter_memory.py <WORDLIST>
```

### Benchmark speed

To test the speed of text censoring against a dataset of paragraphs run

```
python scripts/paragraphs.py
```

Note that this script uses `pytest` and `pytest-benchmark`. If you run the command via `pytest scripts/paragraphs.py` you will have more control over the benchmarking procedures. Read up on [`pytest-benchmark`'s command-line options](https://pytest-benchmark.readthedocs.io/en/latest/usage.html#commandline-options) for more details.

## Limitations

1. Memory usage reported by `memory.py` may vary slightly between runs. Run `memory.py` several times and compute an average for a more accurate memory benchmark.
2. The dataset used by `paragraphs.py` may not be valid for all versions of `better_profanity`. If some words contained in the default word list are removed, some paragraphs' text may not be censored as expected.
