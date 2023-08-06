#!/usr/bin/env python3
# encoding: utf-8

import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

long_description = "TBA"

setuptools.setup(
    name="PyCPU_RAINBOW",
    version="0.42.00",
    author="Scott McCallum (https github.com scott91e1)",
    author_email="262464@195387.com",
    description="A PyCPU for https://rainbow4th.readme.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scott91e1/RAINBOW4TH",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
