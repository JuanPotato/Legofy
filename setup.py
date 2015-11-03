#!/usr/bin/env python

from setuptools import setup

setup(
    name='legofy',
    version="0.0.1",
    packages=["legofy"],
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
    package_data={
        'bricks': ['*.png'],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
)
