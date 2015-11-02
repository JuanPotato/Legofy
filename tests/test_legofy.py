import unittest
import legofy
import os


class LegofyTestCase(unittest.TestCase):

    def test_full_process(self):
        here = os.path.abspath(os.path.dirname(__file__))
        image = os.path.join(here, 'image.jpg')
        legofy.main(image, output='lego_image.png')
        expected = os.path.join(here, 'lego_image.png')
        self.assertTrue(os.path.exists(expected))
