# Legofy [![Build Status](https://travis-ci.org/JuanPotato/Legofy.svg?branch=master)](https://travis-ci.org/JuanPotato/Legofy) [![Coverage Status](https://coveralls.io/repos/JuanPotato/Legofy/badge.svg?branch=master&service=github)](https://coveralls.io/github/JuanPotato/Legofy?branch=master) [![Code Health](https://landscape.io/github/JuanPotato/Legofy/master/landscape.svg?style=flat)](https://landscape.io/github/JuanPotato/Legofy/master) [![Join the chat at https://gitter.im/JuanPotato/Legofy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/JuanPotato/Legofy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


### What is it?
Legofy is a python program that takes a static image or gif and makes it so that it looks as if it was built out of LEGO.

<a href="https://commons.wikimedia.org/wiki/File:Zoysia_grass_flower.jpg">
<img alt="Before" title="Before (The inflorescence of Zoysia grass, a variety of lawn grass. Picture by Hari Krishnan)" height="500" src="legofy/assets/flower.jpg?raw=true">
</a>
<img alt="After" title="After" height="500" src="legofy/assets/flower_lego.png?raw=true">


### Requirements
* Python
* Python modules: Pillow, click
* imagemagick

### Bugs
If you find a bug:
  1. Check in the [open issues](https://github.com/JuanPotato/Legofy/issues) if the bug already exists.
  2. If the bug is not there, create a [new issue](https://github.com/JuanPotato/Legofy/issues/new) with clear steps on how to reproduce it.

### Quickstart
```shell
$ git clone https://github.com/JuanPotato/Legofy.git
$ cd Legofy
$ python setup.py install
$ legofy image.jpg # anywhere
```
Wait! I don't know what any of this means? [Detailed instructions](#installation)

### Usage
```
Usage: legofy [OPTIONS] IMAGE [OUTPUT]

  Legofy an image!

Options:
  --size INTEGER                  Number of bricks the longest side of the legofied image should have.
  --dither / --no-dither          Use dither algorithm to spread the color approximation error.
  --palette [all|effects|mono|solid|transparent]
                                  Palette to use based on real Lego colors.
  --help                          Show this message and exit.
```

#### Palette
There are 3 palettes: solid (33 colors), transparent (14 colors) and effects (4 colors).
You can use one of them or all the 3.
```
$ legofy --palette solid image.jpg
$ legofy --palette transparent image.jpg
$ legofy --palette effects image.jpg
$ legofy --palette all image.jpg
```
There is another one palette, mono, with only 2 colors (black and white...). It's just for test and fun...


### Troubleshooting
#### Mac
 * `ValueError: --enable-zlib requested but zlib not found, aborting.`
   * try `xcode-select --install` in the terminal
 * `ValueError: --enable-jpeg requested but jpeg not found, aborting.`
   * install [libjpeg](http://ethan.tira-thompson.com/Mac_OS_X_Ports.html)
 * `Incompatible library version: libtiff.X requires version X or later, but libjpeg.X provides version X`
   * Follow instructions [here](http://stackoverflow.com/a/22738746/3390376)

### Installation
1. Download and install all requirements
 * python from the [official python website](https://www.python.org/)
 * imagemagick from the [official imagemagick website](https://imagemagick.org/)
2. Download this project by using the download zip button on this page, or running `git clone https://github.com/JuanPotato/Legofy`
 * If you downloaded a zip file, please unzip it
3. Open a command line and navigate to the project folder
4. Run `python setup.py install` while in the project folder
5. You can now use Legofy anywhere, see [usage](#usage) for more help
