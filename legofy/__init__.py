from PIL import Image
from subprocess import call
import shutil
import sys
import os
import copy


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

    r = channels[0].point(lambda color: overlayRed - 100 if (133 - color) > 100 else (overlayRed + 100 if (133 - color) < -100 else overlayRed - (133 - color)))
    g = channels[1].point(lambda color: overlayGreen - 100 if (133 - color) > 100 else (overlayGreen + 100 if (133 - color) < -100 else overlayGreen - (133 - color)))
    b = channels[2].point(lambda color: overlayBlue - 100 if (133 - color) > 100 else (overlayBlue + 100 if (133 - color) < -100 else overlayBlue - (133 - color)))

    channels[0].paste(r)
    channels[1].paste(g)
    channels[2].paste(b)

    return Image.merge(image.mode, channels)

# create a lego brick from a single color
def makeLegoBrick(brickImage, overlayRed, overlayGreen, overlayBlue):
    brickImageCopy = copy.copy(brickImage)
    return applyEffect(brickImageCopy, overlayRed, overlayGreen, overlayBlue)


# create a lego version of an image from an image
def makeLegoImage(baseImage, brick):

    baseWidth, baseHeight = baseImage.size
    basePoa = baseImage.load()

    legoImage = Image.new("RGB", (baseWidth * 30, baseHeight * 30), "white")
    brickImage = Image.open(brick)

    for x in range(baseWidth):
        for y in range(baseHeight):
            bp = basePoa[x, y]
            legoImage.paste(makeLegoBrick(brickImage, bp[0], bp[1], bp[2]), (x * 30, y * 30, (x + 1) * 30, (y + 1) * 30))

    return legoImage

# check if image is animated
def is_animated(im):
    try:
        im.seek(1)
        return True
    except EOFError:
        return False


def main(filename, brick, width=30, height=30, scale=1):
    # open gif to start splitting
    baseImage = Image.open(filename)
    newSize = baseImage.size
    newFilename = '{0}/lego_{1}'.format(*os.path.split(filename))

    if newSize[0] > width or newSize[1] > height:
        if newSize[0] < newSize[1]:
            scale = newSize[1] / height
        else:
            scale = newSize[0] / width
    
        newSize = (int(round(newSize[0] / scale)), int(round(newSize[1] / scale)))

        print(newSize)

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
                makeLegoImage(im, brick).save("./tmp_frames/{0}".format(file))

        # make new gif "convert -delay 10 -loop 0 *.png animation.gif"
        delay = str(baseImage.info["duration"] / 10)
    
        command = "convert -delay {0} -loop 0 ./tmp_frames/*.png {1}".format(delay, newFilename)

        print(command)
        call(command.split(" "))
        print("Creating gif with filename\"lego_{0}\"".format(filename))
        shutil.rmtree('./tmp_frames')

    else:
        # Other image types

        newFilename = newFilename.split(".")
        newFilename[len(newFilename) - 1] = "png"
        newFilename = ".".join(newFilename)
        
        baseImage.convert("RGBA")
        if scale != 1:
            baseImage.thumbnail(newSize, Image.ANTIALIAS)
        print("Static image detected, will now legofy and save as {0}".format(newFilename))
        makeLegoImage(baseImage, brick).save(newFilename)

    print("Finished!")
