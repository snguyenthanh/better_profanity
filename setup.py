import setuptools

from better_profanity import __version__

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="better_profanity",
    version=__version__,
    author="Son Nguyen Thanh",
    author_email="thanhson16198@gmail.com",
    description="A Python library to clean swear words (and their leetspeak) in strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snguyenthanh/better_profanity",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    packages=setuptools.find_packages(),
    data_files=[
        ("wordlist", ["better_profanity/profanity_wordlist.txt"]),
        ("unicode_characters", ["better_profanity/alphabetic_unicode.json"])
    ],
    package_data={"better_profanity": ["profanity_wordlist.txt", "alphabetic_unicode.json"]},
    include_package_data=True
)
