#!/usr/bin/env python3
# encoding: utf-8

import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

long_description = """

Welcome to RETRO, my personal take on the Forth language. This is a modern system primarily targetting desktop, mobile, and servers, though it can also be used on some larger (ARM, MIPS32)
embedded systems.

The language is Forth. It is untyped, uses a stack to pass data between functions called words, and a dictionary which tracks the word names and data structures.

But it's not a traditional Forth. RETRO draws influences from many sources and takes a unique approach to the language.

RETRO has a large vocabulary of words. Keeping a copy of the Glossary on hand is highly recommended as you learn to use RETRO.

http://forth.works/book.html

https://rainbow4th.readme.io

https://github.com/scott91e1/RETROFORTH

"""

setuptools.setup(
    name="RETROFORTH",
    version="0.42.00",
    description="RETROFORTH is a Win64/Win32/Linux/MacOS/UNIX, Python, and C++ distribution of https://sr.ht/~crc_/retroforth / http://www.retroforth.org / http://forth.works/book.html is compatible with Charles Childers's https://github.com/crcx / retroforth. Its big brother is RAINBOW4TH.",
    author="Scott McCallum (https github.com scott91e1)",
    author_email="Scott.McCallum@intermine.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.github.com/scott91e1/RETROFORTH",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
