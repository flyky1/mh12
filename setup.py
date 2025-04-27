#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kiwoom-openapi",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A client library for Kiwoom Securities Open API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kiwoom-openapi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.26.0",
        "websockets>=10.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "numpy>=1.20.0",
        "tabulate>=0.9.0",
    ],
    keywords=[
        "finance",
        "trading",
        "stock",
        "api",
        "kiwoom",
        "kiwoom-securities",
        "openapi",
        "stock-trading",
    ],
) 