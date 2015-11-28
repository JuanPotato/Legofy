'''Unit tests for legofy'''
# They can be run individually, for example:
# nosetests tests.test_legofy:Create.test_legofy_image
import os
import tempfile
import unittest
from PIL import Image

import legofy

TEST_DIR = os.path.realpath(os.path.dirname(__file__))
FLOWER_PATH = os.path.join(TEST_DIR, '..', 'legofy', 'assets', 'flower.jpg')


class Create(unittest.TestCase):
    '''Unit tests that create files.'''

    def setUp(self):
        self.out_path = None

    def tearDown(self):
        if self.out_path:
            os.remove(self.out_path)

    def create_tmpfile(self, suffix):
        '''Creates a temporary file and stores the path in self.out_path'''
        handle, self.out_path = tempfile.mkstemp(prefix='lego_', suffix=suffix)
        os.close(handle)
        self.assertTrue(os.path.exists(self.out_path))
        self.assertTrue(os.path.getsize(self.out_path) == 0)

    def test_legofy_image(self):
        '''Can we legofy a static image?'''
        self.create_tmpfile('.png')
        self.assertTrue(os.path.exists(FLOWER_PATH),
                        "Could not find image : {0}".format(FLOWER_PATH))

        legofy.main(FLOWER_PATH, output_path=self.out_path)
        self.assertTrue(os.path.getsize(self.out_path) > 0)

    def test_legofy_gif(self):
        '''Can we legofy a gif?'''
        self.create_tmpfile('.gif')
        gif_path = os.path.join(TEST_DIR, '..', 'legofy', 'assets', 'bacon.gif')
        self.assertTrue(os.path.exists(gif_path),
                        "Could not find image : {0}".format(gif_path))
        legofy.main(gif_path, output_path=self.out_path)
        self.assertTrue(os.path.getsize(self.out_path) > 0)

    def test_legofy_palette(self):
        '''Can we use a palette?'''
        self.create_tmpfile('.png')
        self.assertTrue(os.path.exists(FLOWER_PATH),
                        "Could not find image : {0}".format(FLOWER_PATH))
        out = self.out_path
        legofy.main(FLOWER_PATH, output_path=out, palette_mode='solid')
        legofy.main(FLOWER_PATH, output_path=out, palette_mode='transparent')
        legofy.main(FLOWER_PATH, output_path=out, palette_mode='effects')
        legofy.main(FLOWER_PATH, output_path=out, palette_mode='mono')
        legofy.main(FLOWER_PATH, output_path=out, palette_mode='all')
        self.assertTrue(os.path.getsize(out) > 0)

    def test_bricks_parameter(self):
        '''Can we specify the --brick parameter and is the file size
           proportional?'''
        self.create_tmpfile('.png')
        legofy.main(FLOWER_PATH, output_path=self.out_path, size=5)
        size5 = os.path.getsize(self.out_path)
        legofy.main(FLOWER_PATH, output_path=self.out_path, size=10)
        size10 = os.path.getsize(self.out_path)
        self.assertTrue(size5 > 0)
        self.assertTrue(size10 > size5)

    def test_small_brick(self):
        '''Test hitting the minimal brick size'''
        self.create_tmpfile('.png')
        legofy.main(FLOWER_PATH, output_path=self.out_path, size=1)
        self.assertTrue(Image.open(self.out_path).size == (30, 30))

    def test_dither_without_palette(self):
        '''Dithering without a palette should still work'''
        self.create_tmpfile('.png')
        legofy.main(FLOWER_PATH, output_path=self.out_path, dither=True)
        self.assertTrue(os.path.getsize(self.out_path) > 0)


class Functions(unittest.TestCase):
    '''Test the behaviour of individual functions'''

    def test_get_new_filename(self):
        '''Test the default output filename generation'''
        # Is the generated path in the same directory?
        new_path = legofy.get_new_filename(FLOWER_PATH)
        self.assertTrue(os.path.dirname(FLOWER_PATH) ==
                        os.path.dirname(new_path))
        # Is the generated path unique?
        self.assertFalse(os.path.exists(new_path),
                         "Should not find image : {0}".format(new_path))
        # Test default file extensions
        self.assertTrue(new_path.endswith('_lego.jpg'))
        new_path = legofy.get_new_filename(FLOWER_PATH, '.gif')
        self.assertTrue(new_path.endswith('_lego.gif'))

    def test_lego_palette_structure(self):
        """Validate lego palettes structured in 3's."""
        legos = legofy.palettes.legos()
        for palette in legos:
            self.assertFalse(len(legos[palette]) % 3)

    def test_lego_palette_length(self):
        """PIL palette requires 768 ints (256 colors * RGB)."""
        legos = legofy.palettes.legos()
        for palette in legos:
            self.assertTrue(len(legofy.palettes.extend_palette(palette)) == 768)


class Failures(unittest.TestCase):
    '''Make sure things fail when they should'''
    def test_bad_image_path(self):
        '''Test invalid image path'''
        fake_path = os.path.join(TEST_DIR, 'fake_image.jpg')
        self.assertFalse(os.path.exists(fake_path),
                         "Should not find image : {0}".format(fake_path))
        self.assertRaises(SystemExit, legofy.main, fake_path)

if __name__ == '__main__':
    unittest.main()
