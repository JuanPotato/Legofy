from __future__ import unicode_literals

from PIL import Image
from subprocess import call
import shutil
import sys
import os
import csv
import math

colors = []

def colorDistance(rgb1, rgb2):
    r1 = rgb1[0]
    r2 = rgb2[0]
    g1 = rgb1[1]
    g2 = rgb2[1]
    b1 = rgb1[2]
    b2 = rgb2[2]

    return math.sqrt(math.pow(r1 - r2, 2) + math.pow(g1 - g2, 2) + math.pow(b1 - b2, 2))

# function that iterates over the gif's frames
def iter_frames(imageToIter):
    try:
        i = 0
        while 1:
            imageToIter.seek(i)
            imframe = imageToIter.copy()
            if i == 0:
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass


# small function to apply an effect over an entire image
def applyEffect(image, overlayRed, overlayGreen, overlayBlue):
    channels = image.split()

    rgb = [overlayRed, overlayGreen, overlayBlue]
    closestrgb = rgb
    min = 1000
    for legorgb in colors:
        legomin = colorDistance(rgb, legorgb)
        if legomin < min:
            min = legomin
            closestrgb = legorgb


    r = channels[0].point(lambda color: closestrgb[0] - 100 if (133 - color) > 100 else (closestrgb[0] + 100 if (133 - color) < -100 else closestrgb[0] - (133 - color)))
    g = channels[1].point(lambda color: closestrgb[1] - 100 if (133 - color) > 100 else (closestrgb[1] + 100 if (133 - color) < -100 else closestrgb[1] - (133 - color)))
    b = channels[2].point(lambda color: closestrgb[2] - 100 if (133 - color) > 100 else (closestrgb[2] + 100 if (133 - color) < -100 else closestrgb[2] - (133 - color)))

    channels[0].paste(r)
    channels[1].paste(g)
    channels[2].paste(b)

    return Image.merge(image.mode, channels)

 
# create a lego brick from a single color
def makeLegoBrick(brickImage, overlayRed, overlayGreen, overlayBlue):
    return applyEffect(brickImage.copy(), overlayRed, overlayGreen, overlayBlue)


# create a lego version of an image from an image
def makeLegoImage(baseImage, brickFilename, width, height):
    brickImage = Image.open(brickFilename)
    baseWidth, baseHeight = baseImage.size
    basePoa = baseImage.load()

    legoImage = Image.new("RGB", (baseWidth * width, baseHeight * height), "white")

    for x in range(baseWidth):
        for y in range(baseHeight):
            bp = basePoa[x, y]
            legoImage.paste(makeLegoBrick(brickImage, bp[0], bp[1], bp[2]), (x * width, y * height, (x + 1) * width, (y + 1) * height))
    
    del basePoa
    
    return legoImage


# check if image is animated
def is_animated(im):
    try:
        im.seek(1)
        return True
    except EOFError:
        return False


def main(filename, brick, palette):
    # open gif to start splitting
    realPath = os.path.realpath(filename)
    if not os.path.isfile(realPath):
        print('File "{0}" was not found.'.format(filename))
        sys.exit(0)
    
    brick = os.path.realpath(brick)
    
    if not os.path.isfile(brick):
        print('Brick asset "{0}" was not found.'.format(brick))
        sys.exit(0)

    if not os.path.isfile(palette):
        print('Palette asset "{0}" was not found.'.format(palette))
        sys.exit(0)

    with open(palette, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rgb = [int(row[0]), int(row[1]), int(row[2])]
            colors.append(rgb)

    baseImage = Image.open(realPath)
    
    newFilename = os.path.split(realPath)
    newFilename = os.path.join(newFilename[0], "lego_{0}".format(newFilename[1]))

    scale = 1
    newSize = baseImage.size
    brickSize = Image.open(brick).size
    
    if newSize[0] > brickSize[0] or newSize[1] > brickSize[1]:
        if newSize[0] < newSize[1]:
            scale = newSize[1] / brickSize[1]
        else:
            scale = newSize[0] / brickSize[0]
    
        newSize = (int(round(newSize[0] / scale)), int(round(newSize[1] / scale)))

    if filename.lower().endswith(".gif") and is_animated(baseImage):
        # Animated GIF

        print("Animated gif detected, will now legofy each frame and recreate the gif and save as lego_{0}".format(filename))
        # check if dir exists, if not, make it
        if not os.path.exists("./tmp_frames/"):
            os.makedirs("./tmp_frames/")

        # for each frame in the gif, save it
        for i, frame in enumerate(iter_frames(baseImage)):
            frame.save('./tmp_frames/frame_{0}.png'.format(("0" * (4 - len(str(i)))) + str(i)), **frame.info)

        # make lego images from gif
        for file in os.listdir("./tmp_frames"):
            if file.endswith(".png"):
                print("Working on {0}".format(file))
                im = Image.open("./tmp_frames/{0}".format(file)).convert("RGBA")
                if scale != 1:
                    im.thumbnail(newSize, Image.ANTIALIAS)
                makeLegoImage(im, brick, brickSize[0], brickSize[1]).save("./tmp_frames/{0}".format(file))

        # make new gif "convert -delay 10 -loop 0 *.png animation.gif"
        delay = str(baseImage.info["duration"] / 10)
    
        command = "convert -delay {0} -loop 0 ./tmp_frames/*.png {1}".format(delay, newFilename)
        if os.name == "nt":
            MAGICK_HOME = os.environ.get('MAGICK_HOME')
            command = os.path.join(MAGICK_HOME, "convert.exe") + " -delay {0} -loop 0 ./tmp_frames/*.png {1}".format(delay, newFilename)

        print(command)
        call(command.split(" "))
        print("Creating gif with filename\"lego_{0}\"".format(filename))
        shutil.rmtree('./tmp_frames')
    else:

        # Other image types

        newFilename = newFilename.rpartition('.')[0] + '.png'
        
        baseImage.convert("RGBA")
        if scale != 1:
            baseImage.thumbnail(newSize, Image.ANTIALIAS)
        print("Static image detected, will now legofy and save as {0}".format(newFilename))
        makeLegoImage(baseImage, brick, brickSize[0], brickSize[1]).save(newFilename)

    print("Finished!")
