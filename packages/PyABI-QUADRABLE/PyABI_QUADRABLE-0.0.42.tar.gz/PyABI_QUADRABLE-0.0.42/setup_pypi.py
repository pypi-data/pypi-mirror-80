#!/usr/bin/env python3
# encoding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyABI_QUADRABLE",
    version="0.0.42",
    author="Scott McCallum (https github.com scott91e1)",
    author_email="262464@195387.com",
    description="PyABI verion Quadrable an authenticated multi-version database. It is implemented as a sparse binary merkle tree with compact partial-tree proofs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyABI/PyABI_QUADRABLE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
