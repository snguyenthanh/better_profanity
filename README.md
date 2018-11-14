better_profanity
---
*A Python library to clean swear words in strings.*

[![release](https://img.shields.io/badge/dynamic/json.svg?label=release&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fbetter-profanity%2Fjson&query=%24.info.version&colorB=blue)](https://github.com/snguyenthanh/better_profanity/releases/latest)
[![Build Status](https://travis-ci.com/snguyenthanh/better_profanity.svg?branch=master)](https://travis-ci.com/snguyenthanh/better_profanity)
![python](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=popout)](https://github.com/snguyenthanh/better_profanity/blob/master/LICENSE)


Inspired from package [profanity](https://github.com/ben174/profanity) of [Ben Friedland](https://github.com/ben174), this library is much faster than the original one, by using string comparison instead of regex.

## Requirements
To make use of Python static tying, this package only works with `Python 3.6+`.

## Installation

### 1. *Stable* version:
```
$ pip install better_profanity
```

### 2. *Beta* version
```
$ pip install better-profanity==0.3b0
```

## Unicode characters
A huge thanks to [@Derfirm](https://github.com/Derfirm) for adding support for Unicode characters.

Currently, the Unicode support is only available in [*beta* release `0.3-beta.0`](https://pypi.org/project/better-profanity/0.3b0/).

For release `0.3-beta.0`, only Unicode characters from categories `Ll`, `Lu`, `Mc` and `Mn` are added. More on Unicode categories can be found [here][unicode category link].

[unicode category link]: https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)

## Usage
By default, on the first `.censor()` call, `profanity` initializes a set of words, from [profanity_wordlist.txt](./better_profanity/profanity_wordlist.txt), to be used to compare against the input texts. This set of words will be stored in memory (~5MB+).

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

### 2. Censor doesn't care about word dividers (*beta*)
The function `.censor()` also hide words separated not just by an empty space ` ` but also other dividers, such as `_`, `,` and `.`. Except for `@, $, ^, *, &, ", '`.

```
from better_profanity import profanity

if __name__ == "__main__":
    text = "...shit...hello_cat_fuck,,,,123"

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
```
from better_profanity import profanity

if __name__ == "__main__":
    dirty_text = "That l3sbi4n did a very good H4ndjob."

    profanity.contains_profanity(dirty_text)
    # True
```

### 5. Censor swear words with a custom wordlist
The provided list of words will replace the default wordlist.

4 instances of the character in second parameter in `.censor()` will be used to replace the swear words.
```
from better_profanity import profanity

if __name__ == "__main__":
    text = "You p1ec3 of sHit."

    custom_badwords = ['happy', 'jolly', 'merry']
    profanity.load_censor_words(custom_badwords)

    print(profanity.contains_profanity("Fuck you!"))
    # Fuck you

    print(profanity.contains_profanity("Have a merry day! :)"))
    # Have a **** day! :)
```

### 6. Censor Unicode characters (*beta*)

```
from better_profanity import profanity

if __name__ == "__main__":
    bad_text = "Эффекти́вного противоя́дия от я́да фу́гу не существу́ет до сих пор"
    profanity.load_censor_words(["противоя́дия"])

    censored_text = profanity.censor(text)
    print(censored_text)
    # Эффекти́вного **** от я́да фу́гу не существу́ет до сих пор
```
