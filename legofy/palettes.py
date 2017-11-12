# -*- coding: utf-8 -*-

"""
legofy.palettes
---------------

This module contains the `lego` palette mappings.

Color mapping source;
 - http://www.brickjournal.com/files/PDFs/2010LEGOcolorpalette.pdf


    USAGE:
    $ legofy.palettes.legos

See README for project details.
"""
from __future__ import division

LEGOS_LABEL = {
    'white': {'rgb': (244, 244, 244) },
    'brick-yellow': {'rgb': (217, 187, 124) },
    'nougat': {'rgb': (214, 115, 65) },
    'bright-red': { 'rgb': (222, 1, 14) },
    'bright-blue': { 'rgb': (1, 88, 168) },
    'bright-yellow': { 'rgb': (254, 196, 1) },
    'black': { 'rgb': (2, 2, 2) },
    'dark-green': { 'rgb': (1, 124, 41) },
    'bright-green': { 'rgb': (1, 150, 37) },
    'dark-orange': { 'rgb': (168, 62, 22) },
    'transparent': { 'rgb': (238, 238, 238) },
    'transparent-red': { 'rgb': (224, 42, 41) },
    'transparent-light-blue': { 'rgb': (182, 224, 234) },
    'transparent-blue': { 'rgb': (80, 177, 232) },
    'transparent-yellow': { 'rgb': (249, 239, 105) },
    'transparent-flourescent-reddish-orange': { 'rgb': (231, 102, 72) },
    'transparent-green': { 'rgb': (99, 178, 110) },
    'transparent-flourescent-green': { 'rgb': (241, 237, 91) },
    'medium-blue': { 'rgb': (72, 140, 198) },
    'bright-orange': { 'rgb': (231, 100, 25) },
    'transparent-brown': { 'rgb': (166, 145, 130) },
    'transparent-med-reddish-violet': { 'rgb': (238, 157, 195) },
    'transparent-yellowish-green': { 'rgb': (149, 185, 12) },
    'transparent-reddish-violet': { 'rgb': (156, 1, 198) },
    'transparent-bluish-violet': { 'rgb': (156, 149, 199) },
    'silver': { 'rgb': (141, 148, 150) },
    'sand-blue': { 'rgb': (95, 117, 140) },
    'sand-yellow': { 'rgb': (141, 117, 83) },
    'earth-blue': { 'rgb': (1, 38, 66) },
    'earth-green': { 'rgb': (1, 53, 23) },
    'transparent-flourescent-blue': { 'rgb': (206, 227, 246) },
    'metallic-dark-grey': { 'rgb': (73, 63, 59) },
    'sand-green': { 'rgb': (96, 130, 102) },
    'dark-red': { 'rgb': (128, 9, 28) },
    'transparent-bright-orange': { 'rgb': (236, 118, 14) },
    'flame-yellowish-orange': { 'rgb': (244, 155, 1) },
    'reddish-brown': { 'rgb': (92, 29, 13) },
    'medium-stone-grey': { 'rgb': (156, 146, 145) },
    'dark-stone-grey': { 'rgb': (77, 94, 87) },
    'light-stone-grey': { 'rgb': (228, 228, 218) },
    'light-royal-blue': { 'rgb': (135, 192, 234) },
    'bright-purple': { 'rgb': (222, 56, 139) },
    'light-purple': { 'rgb': (238, 157, 195) },
    'cool-yellow': { 'rgb': (255, 255, 153) },
    'medium-lilac': { 'rgb': (45, 22, 120) },
    'light-nougat': { 'rgb': (245, 193, 137) },
    'phosph-green': { 'rgb': (254, 252, 213) },
    'warm-gold': { 'rgb': (170, 127, 46) },
    'dark-brown': { 'rgb': (49, 16, 7) },
    'transparent-bright-green': { 'rgb': (153, 255, 102) },
    'medium-nougat': { 'rgb': (170, 126, 86) }
}

LEGOS = {
    'solid': {
        '024': [0xfe, 0xc4, 0x01],
        '106': [0xe7, 0x64, 0x19],
        '021': [0xde, 0x01, 0x0e],
        '221': [0xde, 0x38, 0x8b],
        '023': [0x01, 0x58, 0xa8],
        '028': [0x01, 0x7c, 0x29],
        '119': [0x95, 0xb9, 0x0c],
        '192': [0x5c, 0x1d, 0x0d],
        '018': [0xd6, 0x73, 0x41],
        '001': [0xf4, 0xf4, 0xf4],
        '026': [0x02, 0x02, 0x02],
        '226': [0xff, 0xff, 0x99],
        '222': [0xee, 0x9d, 0xc3],
        '212': [0x87, 0xc0, 0xea],
        '037': [0x01, 0x96, 0x25],
        '005': [0xd9, 0xbb, 0x7c],
        '283': [0xf5, 0xc1, 0x89],
        '208': [0xe4, 0xe4, 0xda],
        '191': [0xf4, 0x9b, 0x01],
        '124': [0x9c, 0x01, 0xc6],
        '102': [0x48, 0x8c, 0xc6],
        '135': [0x5f, 0x75, 0x8c],
        '151': [0x60, 0x82, 0x66],
        '138': [0x8d, 0x75, 0x53],
        '038': [0xa8, 0x3e, 0x16],
        '194': [0x9c, 0x92, 0x91],
        '154': [0x80, 0x09, 0x1c],
        '268': [0x2d, 0x16, 0x78],
        '140': [0x01, 0x26, 0x42],
        '141': [0x01, 0x35, 0x17],
        '312': [0xaa, 0x7e, 0x56],
        '199': [0x4d, 0x5e, 0x57],
        '308': [0x31, 0x10, 0x07]
        },

    'transparent': {
        '044': [0xf9, 0xef, 0x69],
        '182': [0xec, 0x76, 0x0e],
        '047': [0xe7, 0x66, 0x48],
        '041': [0xe0, 0x2a, 0x29],
        '113': [0xee, 0x9d, 0xc3],
        '126': [0x9c, 0x95, 0xc7],
        '042': [0xb6, 0xe0, 0xea],
        '043': [0x50, 0xb1, 0xe8],
        '143': [0xce, 0xe3, 0xf6],
        '048': [0x63, 0xb2, 0x6e],
        '311': [0x99, 0xff, 0x66],
        '049': [0xf1, 0xed, 0x5b],
        '111': [0xa6, 0x91, 0x82],
        '040': [0xee, 0xee, 0xee]
        },

    'effects': {
        '131': [0x8d, 0x94, 0x96],
        '297': [0xaa, 0x7f, 0x2e],
        '148': [0x49, 0x3f, 0x3b],
        '294': [0xfe, 0xfc, 0xd5]
        },

    'mono': {
        '001': [0xf4, 0xf4, 0xf4],
        '026': [0x02, 0x02, 0x02]
        },
    }


def extend_palette(palette, colors=256, rgb=3):
    """Extend palette colors to 256 rgb sets."""
    missing_colors = colors - len(palette)//rgb
    if missing_colors > 0:
        first_color = palette[:rgb]
        palette += first_color * missing_colors
    return palette[:colors*rgb]


def legos():
    """Build flattened lego palettes."""
    return _flatten_palettes(LEGOS.copy())

def _flatten_palettes(palettes):
    """Convert palette mappings into color list."""
    flattened = {}
    palettes = _merge_palettes(palettes)
    for palette in palettes:
        flat = [i for sub in palettes[palette].values() for i in sub]
        flattened.update({palette: flat})
    return flattened


def _merge_palettes(palettes):
    """Build unified palette using all colors."""
    unified = {}
    for palette in palettes:
        for item in palettes[palette]:
            unified.update({item: palettes[palette][item]})
    palettes.update({'all': unified})
    return palettes
