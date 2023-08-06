#!/usr/bin/env python3
# encoding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCPU_RETRO",
    version="0.0.11",
    author="Scott McCallum (https github.com scott91e1) << Charles Childers (https github.com crcx)",
    author_email="262464@195387.com",
    description="Dispatcher for the RETROFORTH CPU Type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyCPU/PyCPU_RETRO",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
