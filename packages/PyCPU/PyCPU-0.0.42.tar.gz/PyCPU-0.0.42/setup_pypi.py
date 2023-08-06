#!/usr/bin/env python3
# encoding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCPU",
    version="0.0.42",
    author="PyCPU (https github.com scott91e1)",
    author_email="262646@195387.com",
    description="Virtual CPUs Support For Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyCPU/PyCPU",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
