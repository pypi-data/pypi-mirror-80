import unittest
from colourise.main import complement_rgb


class TestComplementaryColours(unittest.TestCase):
    def test_black_complements_black(self):
        r, g, b = 0, 0, 0
        cr, cg, cb = complement_rgb(r, g, b)
        self.assertEqual(cr, 0)
        self.assertEqual(cg, 0)
        self.assertEqual(cb, 0)

    def test_white_complements_white(self):
        r, g, b = 255, 255, 255
        cr, cg, cb = complement_rgb(r, g, b)
        self.assertEqual(cr, 255)
        self.assertEqual(cg, 255)
        self.assertEqual(cb, 255)

    def test_red_complements_magenta(self):
        r, g, b = 255, 0, 0
        cr, cg, cb = complement_rgb(r, g, b)
        self.assertEqual(cr, 0)
        self.assertEqual(cg, 255)
        self.assertEqual(cb, 255)

    def test_blue_complements_yellow(self):
        r, g, b = 0, 0, 255
        cr, cg, cb = complement_rgb(r, g, b)
        self.assertEqual(cr, 255)
        self.assertEqual(cg, 255)
        self.assertEqual(cb, 0)

    def test_yellow_complements_blue(self):
        r, g, b = 255, 255, 0
        cr, cg, cb = complement_rgb(r, g, b)
        self.assertEqual(cr, 0)
        self.assertEqual(cg, 0)
        self.assertEqual(cb, 255)

    def _test_some_green_complements_pinkish(self):
        r, g, b = 60, 145, 78
        cr, cg, cb = complement_rgb(r, g, b)
        self.assertEqual(cr, 255)
        self.assertEqual(cg, 105)
        self.assertEqual(cb, 220)
