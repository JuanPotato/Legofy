from __future__ import unicode_literals

import os
from PIL import Image
import shutil
from subprocess import call
import sys

from legofy import palettes


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


def apply_color_overlay(image, color):
    '''Small function to apply an effect over an entire image'''
    overlay_red, overlay_green, overlay_blue = color
    channels = image.split()

    r = channels[0].point(lambda color: overlay_effect(color, overlay_red))
    g = channels[1].point(lambda color: overlay_effect(color, overlay_green))
    b = channels[2].point(lambda color: overlay_effect(color, overlay_blue))

    channels[0].paste(r)
    channels[1].paste(g)
    channels[2].paste(b)

    return Image.merge(image.mode, channels)

def overlay_effect(color, overlay):
    '''Actual overlay effect function'''
    if color < 33:
        return overlay - 100
    elif color > 233:
        return overlay + 100
    else:
        return overlay - 133 + color

def make_lego_image(thumbnail_image, brick_image):
    '''Create a lego version of an image from an image'''
    base_width, base_height = thumbnail_image.size
    brick_width, brick_height = brick_image.size

    rgb_image = thumbnail_image.convert('RGB')

    lego_image = Image.new("RGB", (base_width * brick_width,
                                   base_height * brick_height), "white")

    for brick_x in range(base_width):
        for brick_y in range(base_height):
            color = rgb_image.getpixel((brick_x, brick_y))
            lego_image.paste(apply_color_overlay(brick_image, color),
                             (brick_x * brick_width, brick_y * brick_height))
    return lego_image


def get_new_filename(file_path, ext_override=None):
    '''Returns the save destination file path'''
    folder, basename = os.path.split(file_path)
    base, extention = os.path.splitext(basename)
    if ext_override:
        extention = ext_override
    new_filename = os.path.join(folder, "{0}_lego{1}".format(base, extention))
    return new_filename


def get_new_size(base_image, brick_image, size=None):
    '''Returns a new size the first image should be so that the second one fits
       neatly in the longest axis'''
    new_size = base_image.size
    if size:
        scale_x, scale_y = size, size
    else:
        scale_x, scale_y = brick_image.size

    if new_size[0] > scale_x or new_size[1] > scale_y:
        if new_size[0] < new_size[1]:
            scale = new_size[1] / scale_y
        else:
            scale = new_size[0] / scale_x

        new_size = (int(round(new_size[0] / scale)),
                    int(round(new_size[1] / scale)))

        if not new_size[0]:
            new_size = (1, new_size[1])

        if not new_size[1]:
            new_size = (new_size[0], 1)

    return new_size


def get_lego_palette(palette_mode):
    '''Gets the palette for the specified lego palette mode'''
    legos = palettes.legos()
    if palette_mode in legos:
        palette = legos[palette_mode]
    else:
        raise "Unkown palette mode : %s" % palette_mode

    # Repeat the first color so that the palette has 256 colors
    first_color = palette[0:3]
    missing_colors = int(256 - len(palette)/3)
    padding = first_color * missing_colors
    palette += padding
    assert len(palette) == 768
    return palette


def apply_thumbnail_effects(image, palette, dither):
    '''Apply effects on the reduced image before Legofying'''
    palette_image = Image.new("P", (1, 1))
    palette_image.putpalette(palette)
    return image.im.convert("P",
                        Image.FLOYDSTEINBERG if dither else Image.NONE,
                        palette_image.im)


def legofy_gif(base_image, brick_image, output_path, size, palette_mode,
               dither):
    '''Legofy an animated GIF'''
    new_size = get_new_size(base_image, brick_image, size)

    tmp_dir = os.path.join(os.path.dirname(__file__), "tmp_frames")
    # Clean up tmp dir if it exists
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    # Resize frames
    frames = []
    for frame in iter_frames(base_image):
        frame.thumbnail(new_size, Image.ANTIALIAS)
        frames.append(frame)

    # Apply palette transformation
    if palette_mode:
        palette = get_lego_palette(palette_mode)
        frames = [apply_thumbnail_effects(frame, palette, dither)
                  for frame in frames]

    # make lego images from gif
    for i, frame in enumerate(frames, 1):
        print("Converting frame : {0}/{1}".format(i, len(frames)))
        save_path = '%s/frame_%04d.png' % (tmp_dir, i)
        make_lego_image(frame, brick_image).save(save_path)

    # make new gif "convert -delay 10 -loop 0 *.png animation.gif"
    delay = str(base_image.info["duration"] / 10)

    command = ["convert", "-delay", delay, "-loop", "0",
               "{0}/*.png".format(tmp_dir), "{0}".format(output_path)]
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


def legofy_image(base_image, brick_image, output_path, size, palette_mode,
                 dither):
    '''Legofy an image'''
    new_size = get_new_size(base_image, brick_image, size)
    base_image.thumbnail(new_size, Image.ANTIALIAS)
    if palette_mode:
        palette = get_lego_palette(palette_mode)
        base_image = apply_thumbnail_effects(base_image, palette, dither)
    make_lego_image(base_image, brick_image).save(output_path)


def main(image_path, output_path=None, size=None,
         palette_mode=None, dither=False):
    '''Legofy image or gif with brick_path mask'''
    image_path = os.path.realpath(image_path)
    if not os.path.isfile(image_path):
        print('Image file "{0}" was not found.'.format(image_path))
        sys.exit(1)

    brick_path = os.path.join(os.path.dirname(__file__), "assets",
                              "bricks", "1x1.png")

    if not os.path.isfile(brick_path):
        print('Brick asset "{0}" was not found.'.format(brick_path))
        sys.exit(1)

    base_image = Image.open(image_path)
    brick_image = Image.open(brick_path)

    if palette_mode:
        print ("LEGO Palette {0} selected...".format(palette_mode.title()))
    elif dither:
        palette_mode = 'all'

    if image_path.lower().endswith(".gif") and base_image.is_animated:
        if os.name == "nt" and os.environ.get('MAGICK_HOME') is None:
            print('Could not find the MAGICK_HOME environment variable.')
            sys.exit(1)

        if output_path is None:
            output_path = get_new_filename(image_path)
        print("Animated gif detected, will now legofy to {0}".format(output_path))
        legofy_gif(base_image, brick_image, output_path, size, palette_mode, dither)
    else:
        if output_path is None:
            output_path = get_new_filename(image_path, '.png')
        print("Static image detected, will now legofy to {0}".format(output_path))
        legofy_image(base_image, brick_image, output_path, size, palette_mode, dither)

    base_image.close()
    brick_image.close()
    print("Finished!")
