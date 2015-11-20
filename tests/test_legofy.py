'''Unit tests for legofy'''
# They can be run individually, for example:
# nosetests tests.test_legofy:Create.test_legofy_image
import os
import tempfile
import unittest

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
                        
        legofy.main(FLOWER_PATH, output_path=self.out_path, palette_mode='solid')
        legofy.main(FLOWER_PATH, output_path=self.out_path, palette_mode='transparent')
        legofy.main(FLOWER_PATH, output_path=self.out_path, palette_mode='effects')
        legofy.main(FLOWER_PATH, output_path=self.out_path, palette_mode='mono')
        legofy.main(FLOWER_PATH, output_path=self.out_path, palette_mode='all')
        self.assertTrue(os.path.getsize(self.out_path) > 0)
        
    def test_bricks_parameter(self):
        self.create_tmpfile('.png')
        legofy.main(FLOWER_PATH, output_path=self.out_path, bricks=5)
        size5 = os.path.getsize(self.out_path)
        legofy.main(FLOWER_PATH, output_path=self.out_path, bricks=10)
        size10 = os.path.getsize(self.out_path)
        self.assertTrue(size5 > 0)
        self.assertTrue(size10 > size5)
  
class Functions(unittest.TestCase):
    '''Test the behaviour of individual functions'''
    def test_get_new_filename(self):
        new_path = legofy.get_new_filename(FLOWER_PATH)
        self.assertTrue(os.path.dirname(FLOWER_PATH) ==
                        os.path.dirname(new_path))
        self.assertFalse(os.path.exists(new_path),
                        "Should not find image : {0}".format(new_path))
        self.assertTrue(new_path.endswith('_lego.jpg'))
        new_path = legofy.get_new_filename(FLOWER_PATH, '.gif')
        self.assertTrue(new_path.endswith('_lego.gif'))
   

class Failures(unittest.TestCase):
    '''Make sure things fail when they should'''
    def test_bad_image_path(self):
        '''Test invalid image path'''
        fake_path = os.path.join(TEST_DIR, 'fake_image.jpg')
        self.assertFalse(os.path.exists(fake_path),
                        "Should not find image : {0}".format(fake_path))
        self.assertRaises(SystemExit, legofy.main, fake_path)
        
    def test_bad_brick_path(self):
        fake_path = os.path.join(TEST_DIR, 'fake_brick.jpg')
        self.assertFalse(os.path.exists(fake_path),
                        "Should not find image : {0}".format(fake_path))
        self.assertRaises(SystemExit, legofy.main, FLOWER_PATH, 'im.jpg', 5, fake_path)

if __name__ == '__main__':
    unittest.main()
