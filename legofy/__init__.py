from __future__ import unicode_literals

import os
from PIL import Image
import shutil
from subprocess import call
import sys


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


def apply_effect(image, color):
    '''Small function to apply an effect over an entire image'''
    overlay_red, overlay_green, overlay_blue = color
    channels = image.split()

    r = channels[0].point(lambda color: overlay_red - 100 if (133 - color) > 100 else (overlay_red + 100 if (133 - color) < -100 else overlay_red - (133 - color)))
    g = channels[1].point(lambda color: overlay_green - 100 if (133 - color) > 100 else (overlay_green + 100 if (133 - color) < -100 else overlay_green - (133 - color)))
    b = channels[2].point(lambda color: overlay_blue - 100 if (133 - color) > 100 else (overlay_blue + 100 if (133 - color) < -100 else overlay_blue - (133 - color)))

    channels[0].paste(r)
    channels[1].paste(g)
    channels[2].paste(b)

    return Image.merge(image.mode, channels)


def make_lego_brick(brick_image, color):
    '''Create a lego brick from a single color'''
    return apply_effect(brick_image.copy(), color)


def make_lego_image(thumbnail_image, brick_image):
    '''Create a lego version of an image from an image'''
    base_width, base_height = thumbnail_image.size
    brick_width, brick_height = brick_image.size

    rgb_image = thumbnail_image.convert('RGB')

    lego_image = Image.new("RGB", (base_width * brick_width, base_height * brick_height), "white")

    for x in range(base_width):
        for y in range(base_height):
            color = rgb_image.getpixel((x, y))
            lego_image.paste(make_lego_brick(brick_image, color), (x * brick_width, y * brick_height))
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


def get_lego_palette(palette_mode):
    '''Gets the palette for the specified lego palette mode'''
    if (palette_mode == 'solid'):
        palette = palette_solid.values()
    elif (palette_mode == 'transparent'):
        palette = palette_transparent.values()
    elif (palette_mode == 'effects'):
        palette = palette_effects.values()
    elif (palette_mode == 'mono'):
        palette = palette_mono.values()
    else:
        # All palettes 
        palette = palette_solid.values() + palette_transparent.values() + palette_effects.values()

    # Flatten array of color triples
    palette = [item for sublist in palette for item in sublist]
    assert len(palette) % 3 == 0
    
    # Repeat the first color so that the palette has 256 colors
    first_color = palette[0:3]
    missing_colors = 256 - len(palette)/3
    padding = first_color * missing_colors
    palette += padding
    assert len(palette) == 768
 
    return palette

def apply_thumbnail_effects(image, palette_mode, dither):
    '''Apply effects on the reduced image before Legofying'''
    if palette_mode:
        palette_image = Image.new("P", (1, 1))
        palette = get_lego_palette(palette_mode)
        palette_image.putpalette(palette)
        return image.im.convert("P",
                            Image.FLOYDSTEINBERG if dither else Image.NONE,
                            palette_image.im)
    return image

def legofy_gif(base_image, brick_image, output_path, bricks, palette_mode):
    '''Legofy an animated GIF'''
    new_size = get_new_size(base_image, brick_image, bricks)

    tmp_dir = os.path.join(os.path.dirname(__file__), "tmp_frames")
    # Clean up tmp dir if it exists
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    # Apply effects on all frames of gif
    frames = []
    for frame in iter_frames(base_image):
        frame.thumbnail(new_size, Image.ANTIALIAS)
        frame = apply_thumbnail_effects(frame, palette_mode, True)
        frames.append(frame)
        
    # make lego images from gif
    for i, frame in enumerate(frames, 1):
        print("Converting frame : {0}/{1}".format(i, len(frames)))
        make_lego_image(frame, brick_image).save('%s/frame_%04d.png' % (tmp_dir, i))

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


def legofy_image(base_image, brick_image, output_path, bricks, palette_mode):
    '''Legofy an image'''
    new_size = get_new_size(base_image, brick_image, bricks)
    base_image.thumbnail(new_size, Image.ANTIALIAS)
    base_image = apply_thumbnail_effects(base_image, palette_mode, True)
    
    make_lego_image(base_image, brick_image).save(output_path)


def main(image_path, output_path=None, bricks=None, brick_path=None, palette_mode=None):
    '''Legofy image or gif with brick_path mask'''
    image_path = os.path.realpath(image_path)
    if not os.path.isfile(image_path):
        print('Image file "{0}" was not found.'.format(image_path))
        sys.exit(1)

    if brick_path is None:
        brick_path = os.path.join(os.path.dirname(__file__), "assets", "bricks", "1x1.png")
    else:
        brick_path = os.path.realpath(brick_path)

    if not os.path.isfile(brick_path):
        print('Brick asset "{0}" was not found.'.format(brick_path))
        sys.exit(1)

    base_image = Image.open(image_path)
    brick_image = Image.open(brick_path)
    if palette_mode:
        print ("LEGO Palette {0} selected...".format(palette_mode.title()))

    if image_path.lower().endswith(".gif") and base_image.is_animated:
        if os.name == "nt" and os.environ.get('MAGICK_HOME') == None:
            print('Could not find the MAGICK_HOME environment variable.')
            sys.exit(1)
        
        if output_path == None:
            output_path = get_new_filename(image_path)
        print("Animated gif detected, will now legofy to {0}".format(output_path))
        legofy_gif(base_image, brick_image, output_path, bricks, palette_mode)
    else:
        if output_path == None:
            output_path = get_new_filename(image_path, '.png')            
        print("Static image detected, will now legofy to {0}".format(output_path))
        legofy_image(base_image, brick_image, output_path, bricks, palette_mode)

    print("Finished!")
