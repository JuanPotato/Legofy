from __future__ import unicode_literals

from PIL import Image
from subprocess import call
import shutil
import sys
import os


def iter_frames(image_to_iter):
    '''Function that iterates over the gif's frames'''
    try:
        i = 0
        while 1:
            image_to_iter.seek(i)
            imframe = image_to_iter.copy()
            if i == 0:
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass


def apply_effect(image, overlay_red, overlay_green, overlay_blue):
    '''Small function to apply an effect over an entire image'''
    channels = image.split()

    r = channels[0].point(lambda color: overlay_red - 100 if (133 - color) > 100 else (overlay_red + 100 if (133 - color) < -100 else overlay_red - (133 - color)))
    g = channels[1].point(lambda color: overlay_green - 100 if (133 - color) > 100 else (overlay_green + 100 if (133 - color) < -100 else overlay_green - (133 - color)))
    b = channels[2].point(lambda color: overlay_blue - 100 if (133 - color) > 100 else (overlay_blue + 100 if (133 - color) < -100 else overlay_blue - (133 - color)))

    channels[0].paste(r)
    channels[1].paste(g)
    channels[2].paste(b)

    return Image.merge(image.mode, channels)


def make_lego_brick(brick_image, overlay_red, overlay_green, overlay_blue):
    '''Create a lego brick from a single color'''
    return apply_effect(brick_image.copy(), overlay_red, overlay_green, overlay_blue)


def make_lego_image(base_image, brick_image):
    '''Create a lego version of an image from an image'''
    base_width, base_height = base_image.size
    brick_width, brick_height = brick_image.size
    base_poa = base_image.load()

    lego_image = Image.new("RGB", (base_width * brick_width, base_height * brick_height), "white")

    for x in range(base_width):
        for y in range(base_height):
            bp = base_poa[x, y]
            lego_image.paste(make_lego_brick(brick_image, bp[0], bp[1], bp[2]), (x * brick_width, y * brick_height, (x + 1) * brick_width, (y + 1) * brick_height))

    del base_poa

    return lego_image


def get_new_filename(file_path, ext_override=None):
    '''Returns the save destination file path'''
    folder, basename = os.path.split(file_path)
    base, extention = os.path.splitext(basename)
    if ext_override:
        extention = ext_override
    new_filename = os.path.join(folder, "{0}_lego{1}".format(base, extention))
    return new_filename


def get_new_size(base_image, scale, brick_image):
    '''Returns a new size the first image should be so that the second one fits neatly in the longest axis'''
    new_size = base_image.size
    brick_size = brick_image.size

    if new_size[0] > brick_size[0] or new_size[1] > brick_size[1]:
        if new_size[0] < new_size[1]:
            divisor = new_size[1] / brick_size[1] / float(scale)
        else:
            divisor = new_size[0] / brick_size[0] / float(scale)

        new_size = (int(round(new_size[0] / divisor)), int(round(new_size[1] / divisor)))

    return new_size


def legofy_gif(base_image, brick_image, output_path):
    '''Legofy an animated GIF'''
    new_size = get_new_size(base_image, brick_image)
    tmp_dir = os.path.join(os.path.dirname(__file__), "tmp_frames")
    # Clean up tmp dir if it exists
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    # for each frame in the gif, save it
    for i, frame in enumerate(iter_frames(base_image), 1):
        frame.save('%s/frame_%04d.png' % (tmp_dir, i), **frame.info)

    # make lego images from gif
    print("Converting {0} frames".format(i))
    for frame in os.listdir(tmp_dir):
        if frame.endswith(".png"):
            print("Working on {0}".format(frame))
            image = Image.open("{0}/{1}".format(tmp_dir, frame)).convert("RGBA")
            if new_size != base_image.size:
                image.thumbnail(new_size, Image.ANTIALIAS)
            make_lego_image(image, brick_image).save("{0}/{1}".format(tmp_dir, frame))

    # make new gif "convert -delay 10 -loop 0 *.png animation.gif"
    delay = str(base_image.info["duration"] / 10)

    command = ["convert", "-delay", delay, "-loop", "0", "{0}/*.png".format(tmp_dir),  "{0}".format(output_path)]
    if os.name == "nt":
        magick_home = os.environ.get('MAGICK_HOME')
        magick = os.path.join(magick_home, "convert.exe")
        command[0] = magick

    print(" ".join(command))
    print("Creating gif \"{0}\"".format(output_path))
    ret_code = call(command)
    if ret_code != 0:
        print("Error creating the gif.")
        sys.exit(1)
    shutil.rmtree(tmp_dir)


def legofy_image(base_image, scale, brick_image, output_path):
    '''Legofy an image'''
    new_size = get_new_size(base_image, scale, brick_image)

    base_image = base_image.convert("RGB")
    if new_size != base_image.size:
        base_image.thumbnail(new_size, Image.ANTIALIAS)

    make_lego_image(base_image, brick_image).save(output_path)


def main(image_path, scale, brick_path=os.path.join(os.path.dirname(__file__), "bricks", "brick.png"), output=None):
    '''Legofy image or gif with brick_path mask'''

    if os.name == "nt" and os.environ.get('MAGICK_HOME') == None:
        print('Could not find the MAGICK_HOME environment variable.')
        sys.exit(1)

    image_path = os.path.realpath(image_path)
    if not os.path.isfile(image_path):
        print('File "{0}" was not found.'.format(image_path))
        sys.exit(1)

    brick_path = os.path.realpath(brick_path)
    if not os.path.isfile(brick_path):
        print('Brick asset "{0}" was not found.'.format(brick_path))
        sys.exit(1)

    if output:
        output = os.path.realpath(output)
        output = os.path.splitext(output)[0]

    base_image = Image.open(image_path)
    brick_image = Image.open(brick_path)

    if image_path.lower().endswith(".gif") and base_image.is_animated:
        output_path = get_new_filename(image_path)

        if output:
            output_path = "{0}.gif".format(output)
        print("Animated gif detected, will now legofy to {0}".format(output_path))
        legofy_gif(base_image, brick_image, output_path)
    else:
        output_path = get_new_filename(image_path, '.png')

        if output:
            output_path = "{0}.png".format(output)
        print("Static image detected, will now legofy to {0}".format(output_path))
        legofy_image(base_image, scale, brick_image, output_path)

    print("Finished!")
