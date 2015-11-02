import unittest
import legofy
import os


class LegofyTestCase(unittest.TestCase):

    def test_full_process(self):
        here = os.path.abspath(os.path.dirname(__file__))
        image = os.path.join(here, 'image.jpg')
        brick = os.path.join(here, 'brick.png')
        legofy.main(image, brick, output='lego_image.png')
        expected = os.path.join(here, 'lego_image.png')
        self.assertTrue(os.path.exists(expected))

    def test_over_under_min(self):
        value = -200
        result = legofy.overUnder(value)
        self.assertEqual(result, -100)

    def test_over_under_max(self):
        value = 200
        result = legofy.overUnder(value)
        self.assertEqual(result, 100)

    def test_over_under_mid(self):
        value = 55
        result = legofy.overUnder(value)
        self.assertEqual(result, value)
