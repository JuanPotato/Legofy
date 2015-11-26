from __future__ import unicode_literals

from PIL import Image, ImageSequence
import sys
import os

# Python 2 and 3 support
# TODO: Proper images2gif version that supports both Py 2 and Py 3 (mostly handling binary data)
if sys.version_info < (3,):
    import legofy.images2gif_py2 as images2gif
else:
    import legofy.images2gif_py3 as images2gif

# http://www.brickjournal.com/files/PDFs/2010LEGOcolorpalette.pdf
PALETTE_SOLID = {
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

PALETTE_TRANSPARENT = {
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

PALETTE_EFFECTS = {
    "131": [0x8d, 0x94, 0x96],
    "297": [0xaa, 0x7f, 0x2e],
    "148": [0x49, 0x3f, 0x3b],
    "294": [0xfe, 0xfc, 0xd5]
}

PALETTE_MONO = {
    "001": [0xf4, 0xf4, 0xf4],
    "026": [0x02, 0x02, 0x02]
}


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
    '''Returns a new size the first image should be so that the second one fits neatly in the longest axis'''
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
    if palette_mode == 'solid':
        palette = PALETTE_SOLID.values()
    elif palette_mode == 'transparent':
        palette = PALETTE_TRANSPARENT.values()
    elif palette_mode == 'effects':
        palette = PALETTE_EFFECTS.values()
    elif palette_mode == 'mono':
        palette = PALETTE_MONO.values()
    elif palette_mode == 'all':
        palette = list(PALETTE_SOLID.values()) + \
            list(PALETTE_TRANSPARENT.values()) + \
            list(PALETTE_EFFECTS.values())
    else:
        raise "Unkown palette mode : %s" % palette_mode

    # Flatten array of color triples
    palette = [item for sublist in palette for item in sublist]
    assert len(palette) % 3 == 0

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

def legofy_gif(base_image, brick_image, output_path, size, palette_mode, dither):
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

        new_size = get_new_size(frame, brick_image, size)
        frame.thumbnail(new_size, Image.ANTIALIAS)
        if palette_mode:
            palette = get_lego_palette(palette_mode)
            frame = apply_thumbnail_effects(frame, palette, dither)
        new_frame = make_lego_image(frame, brick_image)
        frames_converted.append(new_frame)

    # Make use of images to gif function
    images2gif.writeGif(output_path, frames_converted, duration=original_duration/1000.0, dither=0, subRectangles=False)

def legofy_image(base_image, brick_image, output_path, size, palette_mode, dither):
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
