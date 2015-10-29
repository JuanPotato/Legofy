from PIL import Image
from subprocess import call
import shutil
import os


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
def applyEffect(image, effect):
    width, height = image.size
    poa = image.load()
    for x in range(width):
        for y in range(height):
            poa[x, y] = effect(poa[x, y])
    return image


def overUnder(value, min=-100, max=100):
    if value > max:
        return max
    elif value < min:
        return min
    else:
        return value

 
# create a lego brick from a single color
def makeLegoBrick(brick, overlayRed, overlayGreen, overlayBlue):
    # colorizing the brick function
    def colorize(blockColors):
        newRed = overUnder(133 - overlayRed)
        newGreen = overUnder(133 - overlayGreen)
        newBlue = overUnder(133 - overlayBlue)
        
        return (blockColors[0] - newRed, blockColors[1] - newGreen, blockColors[2] - newBlue, 255)
    
    return applyEffect(Image.open(brick), colorize)


# create a lego version of an image from an image
def makeLegoImage(baseImage, brick, width=30, height=30):
    baseWidth, baseHeight = baseImage.size
    basePoa = baseImage.load()

    legoImage = Image.new("RGB", (baseWidth * width, baseHeight * height), "white")

    for x in range(baseWidth):
        for y in range(baseHeight):
            bp = basePoa[x, y]
            legoImage.paste(makeLegoBrick(brick, bp[0], bp[1], bp[2]), (x * width, y * height, (x + 1) * width, (y + 1) * height))
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
    static = filename.lower().endswith(".gif") and is_animated(baseImage)
    path, name = os.path.split(filename)
    if path == "":
        newFilename = 'lego_{0}'.format(name)
    else:
        newFilename = '{0}/lego_{1}'.format(path, name)

    if newSize[0] > 30 or newSize[1] > 30:
        if newSize[0] < newSize[1]:
            scale = newSize[1] / 30
        else:
            scale = newSize[0] / 30
    
        newSize = (int(round(newSize[0] / scale)), int(round(newSize[1] / scale)))

    if static:
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
        newFilename = newFilename.split(".")
        newFilename[len(newFilename) - 1] = "png"
        newFilename = ".".join(newFilename)
        
        baseImage.convert("RGBA")
        if scale != 1:
            baseImage.thumbnail(newSize, Image.ANTIALIAS)
        print("Static image detected, will now legofy and save as {0}".format(newFilename))
        makeLegoImage(baseImage, brick).save(newFilename)

    print("Finished!")
