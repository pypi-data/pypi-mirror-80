import unittest
from colourise.main import rgb2hsl


class TestRGBtoHSL(unittest.TestCase):
    def test_primary_colour_red(self):
        r, g, b = 255, 0, 0
        h, s, l = rgb2hsl(r, g, b)
        self.assertEqual(h, 0.0)
        self.assertEqual(s, 1.0)
        self.assertEqual(l, 0.5)

    def test_primary_colour_green(self):
        r, g, b = 0, 255, 0
        h, s, l = rgb2hsl(r, g, b)
        self.assertEqual(h, 120.0)
        self.assertEqual(s, 1.0)
        self.assertEqual(l, 0.5)

    def test_primary_colour_blue(self):
        r, g, b = 0, 0, 255
        h, s, l = rgb2hsl(r, g, b)
        self.assertEqual(h, 240.0)
        self.assertEqual(s, 1.0)
        self.assertEqual(l, 0.5)

    def test_secondary_colour_cyan(self):
        r, g, b = 0, 255, 255
        h, s, l = rgb2hsl(r, g, b)
        self.assertAlmostEqual(h, 180.0, delta=0.15)
        self.assertEqual(s, 1.0)
        self.assertEqual(l, 0.5)

    def test_secondary_colour_magenta(self):
        r, g, b = 255, 0, 255
        h, s, l = rgb2hsl(r, g, b)
        self.assertAlmostEqual(h, 300.0, delta=0.15)
        self.assertEqual(s, 1.0)
        self.assertEqual(l, 0.5)

    def test_secondary_colour_yellow(self):
        r, g, b = 255, 255, 0
        h, s, l = rgb2hsl(r, g, b)
        self.assertAlmostEqual(h, 60.0, delta=0.15)
        self.assertEqual(s, 1.0)
        self.assertEqual(l, 0.5)

    def test_black(self):
        r, g, b = 0, 0, 0
        h, s, l = rgb2hsl(r, g, b)
        self.assertEqual(s, 0.0)
        self.assertEqual(s, 0.0)
        self.assertEqual(l, 0.0)

    def test_white(self):
        r, g, b = 255, 255, 255
        h, s, l = rgb2hsl(r, g, b)
        self.assertEqual(s, 0.0)
        self.assertEqual(s, 0.0)
        self.assertEqual(l, 1.0)
