'''Unit tests for legofy'''
import os
import tempfile
import unittest

import legofy

TEST_DIR = os.path.realpath(os.path.dirname(__file__))

class CreateFileTestCase(unittest.TestCase):
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
        image_path = os.path.join(TEST_DIR, '..', 'legofy', 'assets', 'flower.jpg')
        self.assertTrue(os.path.exists(image_path),
                        "Could not find image : {0}".format(image_path))

        legofy.main(image_path, output_path=self.out_path)
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
        image_path = os.path.join(TEST_DIR, '..', 'legofy', 'assets', 'flower.jpg')
        self.assertTrue(os.path.exists(image_path),
                        "Could not find image : {0}".format(image_path))

        legofy.main(image_path, output_path=self.out_path, palette_mode='all')
        self.assertTrue(os.path.getsize(self.out_path) > 0)


class FailureCases(unittest.TestCase):
    def test_bad_image_path(self):
        '''Test invalid image path'''
        image_path = os.path.join(TEST_DIR, '..', 'legofy', 'assets', 'fake.jpg')
        self.assertFalse(os.path.exists(image_path),
                        "Could not find image : {0}".format(image_path))
        self.assertRaises(SystemExit, legofy.main, image_path)

if __name__ == '__main__':
    unittest.main()
