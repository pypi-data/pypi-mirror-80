#!/usr/bin/env python3
# encoding: utf-8

import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

long_description = "TBA"

setuptools.setup(
    name="RAINBOW4TH",
    version="0.0.42",
    author="Scott McCallum (https github.com scott91e1)",
    author_email="262464@195387.com",
    description="RAINBOW4TH is a C++/Python/Java14 Powered FORTH Environment Bundled with SQLite/PostgreSQL/libcurl Plus More Built In and Multiple IDEs. Its derived from and feed backs to DOLPHIN RETROFORH.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rainbow4th.readme.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
