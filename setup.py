import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="better_profanity",
    version="0.1",
    author="Son Nguyen Thanh",
    author_email="thanhson16198@gmail.com",
    description="A Python library to clean swear words in strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snguyenthanh/better_profanity",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    data_files=[("wordlist", ["better_profanity/profanity_wordlist.txt"])],
    package_data={"better_profanity": ['profanity_wordlist.txt']},
    include_package_data=True
)
