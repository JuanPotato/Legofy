from __future__ import unicode_literals

from PIL import Image, ImageSequence
from subprocess import call
import shutil
import sys
import os
import legofy.images2gif


'''http://www.brickjournal.com/files/PDFs/2010LEGOcolorpalette.pdf'''
palette_solid = {
    "024": [0xfe, 0xc4, 0x01],
    "106": [0xe7, 0x64, 0x19],
    "021": [0xde, 0x01, 0x0e],
    "221": [0xde, 0x38, 0x8b],
    "023": [0x01, 0x58, 0xa8],
    "028": [0x01, 0x7c, 0x29],
    "119": [0x95, 0xb9, 0x0c],
    "192": [0x5c, 0x1d, 0x0d],
    "018": [0xd6, 0x73, 0x41],
    "001": [0xf4, 0xf4, 0xf4],
    "026": [0x02, 0x02, 0x02],
    "226": [0xff, 0xff, 0x99],
    "222": [0xee, 0x9d, 0xc3],
    "212": [0x87, 0xc0, 0xea],
    "037": [0x01, 0x96, 0x25],
    "005": [0xd9, 0xbb, 0x7c],
    "283": [0xf5, 0xc1, 0x89],
    "208": [0xe4, 0xe4, 0xda],
    "191": [0xf4, 0x9b, 0x01],
    "124": [0x9c, 0x01, 0xc6],
    "102": [0x48, 0x8c, 0xc6],
    "135": [0x5f, 0x75, 0x8c],
    "151": [0x60, 0x82, 0x66],
    "138": [0x8d, 0x75, 0x53],
    "038": [0xa8, 0x3e, 0x16],
    "194": [0x9c, 0x92, 0x91],
    "154": [0x80, 0x09, 0x1c],
    "268": [0x2d, 0x16, 0x78],
    "140": [0x01, 0x26, 0x42],
    "141": [0x01, 0x35, 0x17],
    "312": [0xaa, 0x7e, 0x56],
    "199": [0x4d, 0x5e, 0x57],
    "308": [0x31, 0x10, 0x07]
}

palette_transparent = {
    "044": [0xf9, 0xef, 0x69],
    "182": [0xec, 0x76, 0x0e],
    "047": [0xe7, 0x66, 0x48],
    "041": [0xe0, 0x2a, 0x29],
    "113": [0xee, 0x9d, 0xc3],
    "126": [0x9c, 0x95, 0xc7],
    "042": [0xb6, 0xe0, 0xea],
    "043": [0x50, 0xb1, 0xe8],
    "143": [0xce, 0xe3, 0xf6],
    "048": [0x63, 0xb2, 0x6e],
    "311": [0x99, 0xff, 0x66],
    "049": [0xf1, 0xed, 0x5b],
    "111": [0xa6, 0x91, 0x82],
    "040": [0xee, 0xee, 0xee]
}

palette_effects = {
    "131": [0x8d, 0x94, 0x96],
    "297": [0xaa, 0x7f, 0x2e],
    "148": [0x49, 0x3f, 0x3b],
    "294": [0xfe, 0xfc, 0xd5]
}

palette_mono = {
    "001": [0xf4, 0xf4, 0xf4],
    "026": [0x02, 0x02, 0x02]
}

palette_complete = {
    "all":          [0x02, 0x02, 0x02],
    "solid":        [0x02, 0x02, 0x02],
    "transparent":  [0xa6, 0x91, 0x82],
    "effects":      [0x49, 0x3f, 0x3b],
    "mono":         [0x02, 0x02, 0x02]
}


def apply_effect(image, overlay_red, overlay_green, overlay_blue):
    '''Small function to apply an effect over an entire image'''
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
    if (133 - color) > 100:
        return overlay - 100
    elif 133 - color < - 100:
        return overlay + 100
    else:
        return overlay - (133 - color)


def make_lego_brick(brick_image, overlay_red, overlay_green, overlay_blue):
    '''Create a lego brick from a single color'''
    return apply_effect(brick_image.copy(), overlay_red, overlay_green, overlay_blue)


def make_lego_image(base_image, brick_image, palette):
    '''Create a lego version of an image from an image'''
    base_width, base_height = base_image.size
    brick_width, brick_height = brick_image.size

    base_poa = base_image.convert('RGB')

    if palette:
        base_poa = make_lego_palette(base_poa, palette, False)
        base_poa = base_poa.convert('RGB')

    lego_image = Image.new("RGB", (base_width * brick_width, base_height * brick_height), "white")

    for x in range(base_width):
        for y in range(base_height):
            bp = base_poa.getpixel((x, y))
            lego_image.paste(make_lego_brick(brick_image, bp[0], bp[1], bp[2]), (x * brick_width, y * brick_height))
    return lego_image


def get_new_filename(file_path, ext_override=None):
    '''Returns the save destination file path'''
    folder, basename = os.path.split(file_path)
    base, extention = os.path.splitext(basename)
    if ext_override:
        extention = ext_override
    new_filename = os.path.join(folder, "{0}_lego{1}".format(base, extention))
    return new_filename


def get_new_size(base_image, brick_image, bricks=None):
    '''Returns a new size the first image should be so that the second one fits neatly in the longest axis'''
    new_size = base_image.size
    if bricks:
        scale_x, scale_y = bricks, bricks
    else:
        scale_x, scale_y = brick_image.size

    if new_size[0] > scale_x or new_size[1] > scale_y:
        if new_size[0] < new_size[1]:
            scale = new_size[1] / scale_y
        else:
            scale = new_size[0] / scale_x

        new_size = (int(round(new_size[0] / scale)), int(round(new_size[1] / scale)))

        if not new_size[0]:
            new_size = (1, new_size[1])

        if not new_size[1]:
            new_size = (new_size[0], 1)

    return new_size

def make_lego_palette(image, palette, dither=False):
    '''Converts the image colors to the specified lego palette'''
    palette_use = ()
    palette_image = Image.new("P", (1, 1))

    if (palette == 'solid'):
        palette_selected = dict(palette_solid.items())
    elif (palette == 'transparent'):
        palette_selected = dict(palette_transparent.items())
    elif (palette == 'effects'):
        palette_selected = dict(palette_effects.items())
    elif (palette == 'mono'):
        palette_selected = dict(palette_mono.items())
    else:
        palette_selected = dict(list(palette_solid.items()) + list(palette_transparent.items()) + list(palette_effects.items()))

    for color in palette_selected:
        palette_use = palette_use + tuple(palette_selected[color])

    palette_image.putpalette(palette_use + tuple(palette_complete[palette]) * (256 - int(len(palette_use)/3)))

    return image.im.convert("P", 1 if dither else 0, palette_image.im)

def legofy_gif(base_image, brick_image, output_path, bricks, palette):
    '''Alternative function that legofies animated gifs, makes use of images2gif - uses numpy!'''
    im = base_image

    # Read original image duration
    original_duration = im.info['duration']

    # Split image into single frames
    frames = [frame.copy() for frame in ImageSequence.Iterator(im)]

    # Create container for converted images
    frames_converted = []

    print("Number of frames to convert: " + str(len(frames)))

    # Iterate through single frames
    for i, frame in enumerate(frames, 1):
        print("Converting frame number " + str(i))

        new_size = get_new_size(frame, brick_image, bricks)
        frame = frame.convert("RGB")
        if new_size != frame.size:
            frame.thumbnail(new_size, Image.ANTIALIAS)
        new_frame = make_lego_image(frame, brick_image, palette)
        frames_converted.append(new_frame)

    # Make use of images to gif function
    images2gif.writeGif(output_path, frames_converted, duration=original_duration/1000.0, dither=0, subRectangles=False)

def legofy_image(base_image, brick_image, output_path, bricks, palette):
    '''Legofy an image'''
    new_size = get_new_size(base_image, brick_image, bricks)

    if palette:
        print ("LEGO Palette {0} selected...".format(palette.title()))

    base_image = base_image.convert("RGB")
    if new_size != base_image.size:
        base_image.thumbnail(new_size, Image.ANTIALIAS)

    make_lego_image(base_image, brick_image, palette).save(output_path)


def main(image_path, output=None, bricks=None, brick_path=None, palette=None):
    '''Legofy image or gif with brick_path mask'''

    image_path = os.path.realpath(image_path)
    if not os.path.isfile(image_path):
        print('File "{0}" was not found.'.format(image_path))
        sys.exit(1)

    if brick_path is None:
        brick_path = os.path.join(os.path.dirname(__file__), "assets", "bricks", "1x1.png")
    else:
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
        legofy_gif(base_image, brick_image, output_path, bricks, palette)
    else:
        output_path = get_new_filename(image_path, '.png')

        if output:
            output_path = "{0}.png".format(output)
        print("Static image detected, will now legofy to {0}".format(output_path))
        legofy_image(base_image, brick_image, output_path, bricks, palette)

    print("Finished!")
