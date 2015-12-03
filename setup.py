#!/usr/bin/env python

from setuptools import setup

setup(
    name="legofy",
    version="1.0.0",
    author="Juan Potato",
    author_email="juanpotatodev@gmail.com",
    url="https://github.com/JuanPotato/Legofy",
    description="Make images look as if they are made out of 1x1 LEGO blocks",
    long_description=("Legofy is a python program that takes a static image or"
                      " gif and makes it so that it looks as if it was built "
                      "out of LEGO."),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ],
    license="MIT",
    packages=['legofy'],
    install_requires=['pillow', 'click'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'legofy = legofy.cli:main',
        ],
    },
    package_data={
        'bricks': ['*.png'],
    },
    test_suite="nose.collector",
    tests_require=['nose'],
)
