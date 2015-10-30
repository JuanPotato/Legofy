# Legofy [![Build Status](https://travis-ci.org/JuanPotato/Legofy.svg?branch=master)](https://travis-ci.org/JuanPotato/Legofy)

### What is it?
Legofy is a python program that takes a static image or gif and makes it so that it looks as if it was created by legos.

<img alt="Before" title="Before" height="500" src="https://github.com/JuanPotato/Legofy/blob/master/tests/image.jpg?raw=true">
<img alt="After" title="After" height="500" src="https://github.com/JuanPotato/Legofy/blob/master/tests/lego_image.png?raw=true">

### Requirements
* Python
* Python modules: Pillow, click
* imagemagick ~(except windows, binary included because reasons)~

### Bugs
* nothing

### TODO
* Make an optional argument to only allow official lego colors

### Examples (it is ok if any of the images are not small, the program automatically shrinks them down)
* Need to make new ones, soon

### Installin instructions for Windows
* Install python 3.5 from [python.org](python.org)
* Open command prompt from the start menu `cmd.exe`
* Install Pillow executing `pip install Pillow`
* Install click executing `pip install click`
* You're set!

### Using Legofy in Windows
* Download master `master.zip` and unzip it to `Desktop` or to `c:\`
* Choose an image you'd like to process, for example, flower.jpg
![flower](https://cloud.githubusercontent.com/assets/2467931/10850989/8f72b7a6-7f39-11e5-9dff-64bd953e060e.jpg)
* Navigate to `\Legofy-master\legofy` in explorer
* Paste image in that folder
* Open command prompt from the start meny `cmd.exe`
* Navigate to the `\Legofy-master\legofy`folder by using `cd` command, for example, `cd C:\Legofy-master\legofy`
* Run `cli.py` passing filename as parameter, for example, `python cli.py flower.jpg`
* Output image will appear in the disk root folder, for example, in `C:\`, and will have lego_ prefix, in this particular example it will be `lego_flower.png`
* The result will look like this:
![lego_flower](https://cloud.githubusercontent.com/assets/2467931/10850994/91c58920-7f39-11e5-9912-c6ecdfbf3c5c.png)
* Enjoy!
