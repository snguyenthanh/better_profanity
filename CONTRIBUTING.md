# Contributing to better_profanity

It is so nice you wanna contribute to this repository. Thank you very much.

You may contribute in several ways like:

* Creating new features
* Fixing bugs
* Improving documentation and examples

## Table of contents
* [Develop](#develop)
* [Run tests](#run-tests)
* [Report a bug](#report-a-bug)
* [Request a feature](#request-a-feature)
* [Commit message](#commit-message)
* [Code style](#code-style)


## Develop

The main API interface is in [profanity.py](./better_profanity/profanity.py), which will call
the complexed processing functions in [utils.py](./better_profanity/utils.py)

The [alphabetic_unicode.json](./better_profanity/alphabetic_unicode.json) contains the Unicode characters (from categories `Ll`, `Lu`, `Mc` and `Mn`). More on Unicode categories can be found [here][unicode category link].

[unicode category link]: https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)

The [profanity_wordlist.txt](./better_profanity/profanity_wordlist.txt) contains all the swear words to be censored.

The [tests.py](./tests.py) is for now the only unit test file in the project.

## Run tests

This package uses [unittest](https://docs.python.org/3/library/unittest.html) for testing.

### 1. Run all tests
```
$ python tests.py
```

### 2. Run all tests in a class
For example, run all test cases in class [ProfanityTest]((./tests.py#L6):
```
$ python -m unittest tests.ProfanityTest
```

### 3. Run a specific test case
For example, run the test [test_censorship_empty_text](./tests.py#L53) in class [ProfanityTest]((./tests.py#L6):
```
$ python -m unittest tests.ProfanityTest.test_censorship_empty_text
```

## Report a bug

Use the [GitHub issue tracker](https://github.com/snguyenthanh/better_profanity/issues) to report any bug you find.
Bugs description should include:

* How to reproduce the bug;
* Easy to understand title;

Would be nice to have some code showing how to reproduce the code, you may use [gist](https://gist.github.com) for uploading your example code.

## Request a feature

Use the [GitHub issue tracker](https://github.com/snguyenthanh/better_profanity/issues) to request a new feature.

## Commit message

Commit messages should includes GitHub number reference and a imperative easy to understand sentence.

## Code style

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 484](https://www.python.org/dev/peps/pep-0484/) for *Python*.

---

Thank you for reading this.

Give this repo a star and/or share it with your friends.
