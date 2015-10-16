#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='legofy',
    version="0.0.0",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=['pillow', 'click'],
    include_package_data=True,
    maintainer='Juan Potato',
    description=('Make any image or GIF LEGOFIED!'),
    url='https://github.com/JuanPotato/Legofy',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'legofy = legofy.cli:main',
        ],
    },
)
