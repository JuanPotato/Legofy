# Legofy [![Build Status](https://travis-ci.org/JuanPotato/Legofy.svg?branch=master)](https://travis-ci.org/JuanPotato/Legofy) [![Join the chat at https://gitter.im/JuanPotato/Legofy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/JuanPotato/Legofy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=6G74RZQ9NWYE6&lc=US&item_name=Legofy%20%2d%20Donations&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted)

### What is it?
Legofy is a python program that takes a static image or gif and makes it so that it looks as if it was built out of LEGO.

<img alt="Before" title="Before" height="500" src="legofy/assets/flower.jpg?raw=true">
<img alt="After" title="After" height="500" src="legofy/assets/flower_lego.png?raw=true">

### Requirements
* Python
* Python modules: Pillow, click
* imagemagick

### Bugs
* If you find a bug, please message me on [Reddit](http://www.reddit.com/message/compose/?to=juan_potato), [Imgur](http://imgur.com/user/juanpotato), [Telegram](https://telegram.me/awkward_potato), or [email me](mailto:juanpotatodev@gmail.com)

### TODO
* Make an optional argument to only allow official lego colors

### Quickstart
```shell
$ git clone https://github.com/JuanPotato/Legofy.git
$ cd Legofy
$ python setup.py install
$ legofy image.jpg # anywhere
```

### Troubleshooting
#### Mac
 * `ValueError: --enable-zlib requested but zlib not found, aborting.`   
   * try `xcode-select --install` in the terminal
 * `ValueError: --enable-jpeg requested but jpeg not found, aborting.`
   * install [libjpeg](http://ethan.tira-thompson.com/Mac_OS_X_Ports.html)
 * `Incompatible library version: libtiff.X requires version X or later, but libjpeg.X provides version X`
   * Follow instructions [here](http://stackoverflow.com/a/22738746/3390376)
