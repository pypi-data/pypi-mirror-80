#!/usr/bin/env python3
# encoding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyABI_CHAISCRIPT",
    version="0.0.42",
    author="Scott McCallum (https github.com scott91e1)",
    author_email="Scott.McCallum@intermine.com",
    description="PyABI_CHIASCRIPT Implements the ChiaScript C++ Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyABI/PyABI_CHAISCRIPT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
