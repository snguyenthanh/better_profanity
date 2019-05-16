# better_profanity
*A Python library to clean swear words (and their leetspeak) in strings*

[![release](https://img.shields.io/badge/dynamic/json.svg?label=release&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fbetter-profanity%2Fjson&query=%24.info.version&colorB=blue)](https://github.com/snguyenthanh/better_profanity/releases/latest)
[![Build Status](https://travis-ci.com/snguyenthanh/better_profanity.svg?branch=master)](https://travis-ci.com/snguyenthanh/better_profanity)
![python](https://img.shields.io/badge/python-3.5%2B-blue.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=popout)](https://github.com/snguyenthanh/better_profanity/blob/master/LICENSE)


Inspired from package [profanity](https://github.com/ben174/profanity) of [Ben Friedland](https://github.com/ben174), this library is significantly faster than the original one, by using string comparison instead of regex.

It supports [modified spellings](https://en.wikipedia.org/wiki/Leet) (such as `p0rn`, `h4ndjob`, `handj0b` and `b*tch`).

## Requirements
To make use of static typing and many relevant optimisations, this package only works with `Python 3.5+`.

## Installation
```
$ pip install better_profanity
```

## Unicode characters

Only Unicode characters from categories `Ll`, `Lu`, `Mc` and `Mn` are added. More on Unicode categories can be found [here][unicode category link].

[unicode category link]: https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)

Not all languages are supported yet, such as *Chinese*.

## Wordlist
Most of the words in the default [wordlist](./better_profanity/profanity_wordlist.txt) are referred from [Full List of Bad Words and Top Swear Words Banned by Google](https://github.com/RobertJGabriel/Google-profanity-words).

The wordlist contains a total of __106,992 words__, including 317 words from the default [profanity_wordlist.txt](./better_profanity/profanity_wordlist.txt) and their variants by modified spellings.

Its total size in memory is 10.49+MB.

## Usage
By default, on the first `.censor()` call, function `.load_censor_words()` generates all possible [leetspeak](https://en.wikipedia.org/wiki/Leet) words, from [profanity_wordlist.txt](./better_profanity/profanity_wordlist.txt), to be used to compare against the input texts.  The full mapping of the library can be found in [profanity.py](./better_profanity/profanity.py#L9-L18).

For example, the word `handjob` would be loaded into:

```
'handjob', 'handj*b', 'handj0b', 'handj@b', 'h@ndjob', 'h@ndj*b', 'h@ndj0b', 'h@ndj@b',
'h*ndjob', 'h*ndj*b', 'h*ndj0b', 'h*ndj@b', 'h4ndjob', 'h4ndj*b', 'h4ndj0b', 'h4ndj@b'
```

### 1. Censor swear words from a text
By default, `profanity` replaces each swear words with 4 asterisks `****`.

```
from better_profanity import profanity

if __name__ == "__main__":
    text = "You p1ec3 of sHit."

    censored_text = profanity.censor(text)
    print(censored_text)
    # You **** of ****.
```

### 2. Censor doesn't care about word dividers
The function `.censor()` also hide words separated not just by an empty space ` ` but also other dividers, such as `_`, `,` and `.`. Except for `@, $, *, ", '`.

```
from better_profanity import profanity

if __name__ == "__main__":
    text = "...sh1t...hello_cat_fuck,,,,123"

    censored_text = profanity.censor(text)
    print(censored_text)
    # "...****...hello_cat_****,,,,123"
```

### 3. Censor swear words with custom character
4 instances of the character in second parameter in `.censor()` will be used to replace the swear words.

```
from better_profanity import profanity

if __name__ == "__main__":
    text = "You p1ec3 of sHit."

    censored_text = profanity.censor(text, '-')
    print(censored_text)
    # You ---- of ----.
```

### 4. Check if the string contains any swear words
Function `.contains_profanity()` return `True` if any words in the given string has a word existing in the wordlist.

```
from better_profanity import profanity

if __name__ == "__main__":
    dirty_text = "That l3sbi4n did a very good H4ndjob."

    profanity.contains_profanity(dirty_text)
    # True
```

### 5. Censor swear words with a custom wordlist
Function `.load_censor_words()` takes a `List` of strings as censored words.
The provided list will replace the default wordlist.

```
from better_profanity import profanity

if __name__ == "__main__":
    custom_badwords = ['happy', 'jolly', 'merry']
    profanity.load_censor_words(custom_badwords)

    print(profanity.contains_profanity("Fuck you!"))
    # Fuck you

    print(profanity.contains_profanity("Have a merry day! :)"))
    # Have a **** day! :)
```

### 6. Censor Unicode characters
No extra steps needed!

```
from better_profanity import profanity

if __name__ == "__main__":
    bad_text = "Эффекти́вного противоя́дия от я́да фу́гу не существу́ет до сих пор"
    profanity.load_censor_words(["противоя́дия"])

    censored_text = profanity.censor(text)
    print(censored_text)
    # Эффекти́вного **** от я́да фу́гу не существу́ет до сих пор
```

## Limitations

1. As the library compares each word by characters, the censor could easily be bypassed by adding any character(s) to the word:

```
profanity.censor('I just have sexx')
# returns 'I just have sexx'

profanity.censor('jerkk off')
# returns 'jerkk off'
```

2. Any word in [wordlist](https://github.com/snguyenthanh/better_profanity/blob/master/better_profanity/profanity_wordlist.txt) that have non-space separators cannot be recognised, such as `s & m`, and therefore, won't be filtered out. This problem was raised in [issue #5](https://github.com/snguyenthanh/better_profanity/issues/5).

## Testing
```
$ python tests.py
```

## Versions

- [v0.3.4](https://github.com/snguyenthanh/better_profanity/releases/tag/0.3.4) - Add significantly more swear words.
- [v0.3.3](https://github.com/snguyenthanh/better_profanity/releases/tag/0.3.3) - Fix incompatibility with Python 3.5.
- [v0.3.2](https://github.com/snguyenthanh/better_profanity/releases/tag/0.3.2) - Fix a typo in documentation.
- [v0.3.1](https://github.com/snguyenthanh/better_profanity/releases/tag/0.3.1) - Remove unused dependencies.
- [v0.3.0](https://github.com/snguyenthanh/better_profanity/releases/tag/0.3.0) - Add support for Unicode characters (Categories: Ll, Lu, Mc and Mn) [#2](https://github.com/snguyenthanh/better_profanity/pull/2).
- [v0.2.0](https://github.com/snguyenthanh/better_profanity/releases/tag/0.2) - Bug fix + faster censoring
- [v0.1.0](https://github.com/snguyenthanh/better_profanity/releases/tag/v0.1) - Initial release

## Contributing
Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Special thanks to
- [Andrew Grinevich](https://github.com/Derfirm) - Add support for Unicode characters.

## Acknowledgments
- [Ben Friedland](https://github.com/ben174) - For the inspiring package [profanity](https://github.com/ben174/profanity).
