"""Benchmarks how fast better_profanity censors large bodies of text"""

import os
import pytest

from better_profanity import profanity


def trial(benchmark, dataset):
    # Load original text and its censored counterpart.
    root = os.path.join(os.path.dirname(__file__), "../data/paragraphs/")
    root = os.path.abspath(root)
    data_dir = os.path.join(root, dataset)
    original_path = os.path.join(data_dir, "original.txt")
    censored_path = os.path.join(data_dir, "censored.txt")
    assert os.path.isfile(original_path)
    assert os.path.isfile(censored_path)
    with open(original_path) as f:
        original = f.read()
    with open(censored_path) as f:
        expected_censored = f.read()

    # Benchmark the censor operation.
    actual_censored = benchmark(profanity.censor, original)
    assert actual_censored == expected_censored


def test_1para_0per(benchmark):
    # 1 paragraph, 0% profanity
    trial(benchmark, "0001paras-000per")


def test_1para_5per(benchmark):
    # 1 paragraph, 5% profanity
    trial(benchmark, "0001paras-005per")


def test_1para_50per(benchmark):
    # 1 paragraph, 50% profanity
    trial(benchmark, "0001paras-050per")


def test_1para_100per(benchmark):
    # 1 paragraph, 100% profanity
    trial(benchmark, "0001paras-100per")


def test_10para_0per(benchmark):
    # 10 paragraphs, 0% profanity
    trial(benchmark, "0010paras-000per")


def test_10para_5per(benchmark):
    # 10 paragraphs, 5% profanity
    trial(benchmark, "0010paras-005per")


def test_10para_50per(benchmark):
    # 10 paragraphs, 50% profanity
    trial(benchmark, "0010paras-050per")


def test_10para_100per(benchmark):
    # 10 paragraphs, 100% profanity
    trial(benchmark, "0010paras-100per")


def test_100para_5per(benchmark):
    # 100 paragraphs, 5% profanity
    trial(benchmark, "0100paras-005per")


if __name__ == "__main__":
    pytest.main([__file__])
