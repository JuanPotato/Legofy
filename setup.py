#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='legoify',
    version="0.0.0",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=['pillow', 'click'],
    include_package_data=True,
    maintainer='Juan Potato',
    description=('Make any image or GIF LEGOIFIED!'),
    url='https://github.com/JuanPotato/Gif-Lego-ify',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'legoify = legoify.cli:main',
        ],
    },
)
