better_profanity
---
*A Python library to clean swear words in strings.*

[![release](https://img.shields.io/badge/release-v0.1-blue.svg)](https://github.com/snguyenthanh/better_profanity/releases/tag/v0.1)
![python](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=popout)](https://github.com/snguyenthanh/better_profanity/blob/master/LICENSE)


Inspired from package [profanity](https://github.com/ben174/profanity) of [Ben Friedland](https://github.com/ben174), this library only supports **English** language and is much faster than the original one, by using string comparison instead of regex.

## Requirements
To make use of Python static tying, this package only works with `Python 3.6+`.

## Note for non-English words
Due to the library's algorithm, it (now) only supports [ASCII](https://docs.python.org/3/library/string.html#string.ascii_letters) characters.

Words, such as `аушвиц and หญิงชาติชั่ว`, will fails to be checked.

## Usage
By default, on the first `.censor()` call, `profanity` initializes a set of words, from [profanity_wordlist.txt](./better_profanity/profanity_wordlist.txt), to be used to compare against the input texts. This set of words will be stored in memory (~5MB+).

### 1. Censor swear words from a text
By default, `profanity` replaces each swear words with 4 asterisks `****`.

```
from better_profanity import profanity

if __name__ == "__main__":
    text = "You p1ec3 of sHit."

    censored_text = profanity.censor(text)
    print(censored_text)    # You **** of ****.
```

### 2. Censor swear words with custom character
4 instances of the character in second parameter in `.censor()` will be used to replace the swear words.
```
from better_profanity import profanity

if __name__ == "__main__":
    text = "You p1ec3 of sHit."

    censored_text = profanity.censor(text, '-')
    print(censored_text)    # You ---- of ----.
```

### 3. Check if the string contains any swear words
```
from better_profanity import profanity

if __name__ == "__main__":
    dirty_text = "That l3sbi4n did a very good H4ndjob."

    profanity.contains_profanity(dirty_text) # True
```

### 4. Censor swear words with a custom wordlist
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
