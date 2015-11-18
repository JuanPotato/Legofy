# Legofy [![Build Status](https://travis-ci.org/JuanPotato/Legofy.svg?branch=master)](https://travis-ci.org/JuanPotato/Legofy) [![Coverage Status](https://coveralls.io/repos/niroyb/Legofy/badge.svg?branch=coverage&service=github)](https://coveralls.io/github/niroyb/Legofy?branch=coverage) [![Join the chat at https://gitter.im/JuanPotato/Legofy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/JuanPotato/Legofy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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

### Options
 * `--bricks number` - specify the largest amount of bricks a side of the resulting image should have. (eg. make the legofied image bigger)
 * `--brick brick` - specify the brick asset to be used in legofying. Should be a 30x30 greyscale image close to 128,128,128 as the base color.
 * `--palette` - specify the palette used, allows you to use only lego colors, see below.

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
