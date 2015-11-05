from __future__ import unicode_literals

from PIL import Image
from subprocess import call
import shutil
import sys
import os

#with open('brickColor.json') as data:
colors = [
    (255, 255, 255),  # 1: white
    (217, 187, 123),  # 5: brick yellow
    (214, 114, 64),  # 18: nougat
    (222, 0, 13),  # 21: bright red
    (0, 87, 168),  # 23: bright blue
    (254, 196, 0),  # 24: bright yellow
    (1, 1, 1),  # 26: black
    (0, 123, 40),  # 28: dark green
    (0, 150, 36),  # 37: bright green
    (168, 61, 21),  # 38: dark orange
    (71, 140, 198),  # 102: medium blue
    (231, 99, 24),  # 106: bright orange
    (149, 185, 11),  # 119: bright yellowish green
    (156, 0, 107),  # 124: bright reddish violet
    (94, 116, 140),  # 135: sand blue
    (141, 116, 82),  # 138: sand yellow
    (0, 37, 65),  # 140: earth blue
    (0, 52, 22),  # 141: earth green
    (95, 130, 101),  # 151: sand green
    (128, 8, 27),  # 154: dark red
    (244, 155, 0),  # 191: flame yellowish orange
    (91, 28, 12),  # 192: reddish brown
    (156, 146, 145),  # 194: medium stone grey
    (76, 81, 86),  # 199: dark stone grey
    (228, 228, 218),  # 208: light stone grey
    (135, 192, 234),  # 212: light royal blue
    (222, 55, 139),  # 221: bright purple
    (238, 157, 195),  # 222: light purple
    (255, 255, 153),  # 226: cool yellow
    (44, 21, 119),  # 268: medium lilac
    (245, 193, 137),  # 283: light nougat
    (48, 15, 6),  # 308: dark brown
    (170, 125, 85),  # 312: medium nougat
    (70, 155, 195),  # 321: dark azur
    (104, 195, 226),  # 322: medium azur
    (211, 242, 234),  # 323: aqua
    (160, 110, 185),  # 324: medium lavender
    (205, 164, 222),  # 325: lavender
    (245, 243, 215),  # 329: white glow
    (226, 249, 154),  # 326: spring yellowish green
    (119, 119, 78),  # 330: olice green
    (150, 185, 59),  # 331: medium yellowish green
]
#    color = json.load(data)

#color = [(int(i['red']), int(i['green']), int(i['blue'])) for i in color ]



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

def getNearestColor(rgbTuple):
    d = {}
    for i in xrange(len(colors)):
       c = map(lambda i,j:i-j, colors[i],rgbTuple)
       c = sum([j**2 for j in c]) 
                                    
       d[c] = colors[i]

    return d[min(d.keys())]

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
    return applyEffect(brickImage.copy(), overlayRed, overlayGreen, overlayBlue)


# create a lego version of an image from an image
def makeLegoImage(baseImage, brickFilename, width, height):
    brickImage = Image.open(brickFilename)
    baseWidth, baseHeight = baseImage.size
    basePoa = baseImage.load()

    legoImage = Image.new("RGB", (baseWidth * width, baseHeight * height), "white")

    for x in range(baseWidth):
        for y in range(baseHeight):
            bp = getNearestColor(basePoa[x, y])
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


def main(filename, brick=os.path.join(os.path.dirname(__file__), "bricks", "brick.png")):
    # open gif to start splitting
    realPath = os.path.realpath(filename)
    if not os.path.isfile(realPath):
        print('File "{0}" was not found.'.format(filename))
        sys.exit(0)
    
    brick = os.path.realpath(brick)
    
    if not os.path.isfile(brick):
        print('Brick asset "{0}" was not found.'.format(brick))
        sys.exit(0)

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
