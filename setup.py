#!/usr/bin/env python3
"""
Setup script for Aurora Nowcast NZ
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aurora-nz-nowcast",
    version="1.0.0",
    author="Aurora Nowcast NZ Team",
    description="Real-time aurora visibility alerts for New Zealand using GeoNet data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jajera/aurora-nz-nowcast",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "aurora-nowcast=backend.geonet_data:main",
        ],
    },
)
