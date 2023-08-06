import unittest
from colourise.main import hsl2rgb


class TestHSLtoRGB(unittest.TestCase):
    def test_primary_colour_red(self):
        h, s, l = 0, 1, 0.5
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 255)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)

    def test_primary_colour_green(self):
        h, s, l = 120, 1, 0.5
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 0)
        self.assertEqual(g, 255)
        self.assertEqual(b, 0)

    def test_primary_colour_blue(self):
        h, s, l = 240, 1, 0.5
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 0)
        self.assertEqual(g, 0)
        self.assertEqual(b, 255)

    def test_secondary_colour_cyan(self):
        h, s, l = 180, 1, 0.5
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 0)
        self.assertEqual(g, 255)
        self.assertEqual(b, 255)

    def test_secondary_colour_yellow(self):
        h, s, l = 60, 1, 0.5
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 255)
        self.assertEqual(g, 255)
        self.assertEqual(b, 0)

    def test_secondary_colour_magenta(self):
        h, s, l = 300, 1, 0.5
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 255)
        self.assertEqual(g, 0)
        self.assertEqual(b, 255)

    def test_black(self):
        h, s, l = 0, 0, 0
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 0)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)

    def test_white(self):
        h, s, l = 0, 0, 1
        r, g, b = hsl2rgb(h, s, l)
        self.assertEqual(r, 255)
        self.assertEqual(g, 255)
        self.assertEqual(b, 255)
