"""This module contains a few functions that allow operations on colours.
For instance, :meth:`hsl2rbg` converts HSL values (hue, saturation, and
lightness) to RGB values (Red, Green, Blue).

:meth:`rgb2hsl` performs the reverse operation.

:meth:`complement_hsl` calculates the complement of a colour when the
input is provided as a HSL colour. Absolutely no validation of the input
is done by this function, so use it with care.

:meth:`complement_rgb` calculates the complement of a colour when the
input is provided as an RGB colour. It uses the aforementioned
:meth:`complement_hsl` for the actual calculation. This method, however,
does provide validation of the input.
"""


def hsl2rgb(h=0.0, s=0.0, l=0.0):
    """Convert any HSL value to RGB.

    By "any" value we mean:
        0 <= h <= 360, 0 <= s <= 1, and 0 <= l <= 1

    A ValueError is raised if this precondition is not met for the input.

    :param h: Hue
    :param s: Saturation
    :param l: Lightness
    :return: Tuple containing R, G, B values
    :raise ValueError: if input is invalid
    """
    if not (0 <= h <= 360 and 0 <= s <= 1 and 0 <= l <= 1):
        raise ValueError('Invalid input.')

    r, g, b = _norm_hsl2rgb(h, s, l)
    return r * 255, g * 255, b * 255


def rgb2hsl(r=0, g=0, b=0):
    """Convert RGB colours to HSL.

    The input must follow these conditions:
        0 <= r <= 255, 0 <= g <= 255, and 0 <= b <= 255

    A ValueError is raised if these conditions are not met.

    :param r: Red as web colour (0..255)
    :param g: Green as web colour (0..255)
    :param b: Blue as web colour (0..255)
    :return: Tuple containing H, S, L values
    :raise ValueError: if input is invalid, e.g., not within allowed range
    """
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError('Invalid input. RGB Values must be between 0..255.')

    return _norm_rgb2hsl(r=r/255, g=g/255, b=b/255)


def _norm_hsl2rgb(h, s, l):
    """Convert HSL to RGB colours. This function assumes the input has
    been sanitised and does no validation on the input parameters.

    This calculation has been adapted from Wikipedia:
    https://en.wikipedia.org/wiki/HSL_and_HSV#To_RGB

    :param h: Hue
    :param s: Saturation
    :param l: Lightness
    :return: A tuple containing R, G, B colours
    """
    C = (1 - abs(2 * l - 1)) * s
    m = l - C / 2
    h_ = h / 60.0  # H' is not necessarily an integer
    X = C * (1 - abs(h_ % 2 - 1))
    r, g, b = 0, 0, 0
    if 0 <= h_ <= 1:
        r, g, b = C, X, 0
    elif 1 < h_ <= 2:
        r, g, b = X, C, 0
    elif 2 < h_ <= 3:
        r, g, b = 0, C, X
    elif 3 < h_ <= 4:
        r, g, b = 0, X, C
    elif 4 <= h_ <= 5:
        r, g, b = C, 0, X
    elif 5 < h_ <= 6:
        r, g, b = X, 0, C

    return r + m, g + m, b + m


def _norm_rgb2hsl(r, g, b):
    """Convert normalised RGB colours to HSL. This function assumes the input
    has been sanitised and does no validation on the input parameters.

    This calculation has been adapted from Wikipedia:
    https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB

    :param r: Red as normalised colour (0 .. 1.0)
    :param g: Green as normalised colour (0 .. 1.0)
    :param b: Blue as normalised colour (0 .. 1.0)
    :return: Tuple containing H, S, L values
    """
    V = X_max = max(r, g, b)
    X_min = min(r, g, b)
    C = X_max - X_min
    L = (X_max + X_min) / 2
    H = 0
    if C > 0:
        if V == r:
            H = 60.0 * (g - b) / C
        elif V == g:
            H = 120.0 + 60.0 * (b - r) / C
        elif V == b:
            H = 240.0 + 60.0 * (r - g) / C

    S = 0.0
    if 0.0 < L < 1.0:
        S = (V - L) / min(L, 1-L)

    return H % 360.0, S, L


def complement_hsl(h=0.0, s=0.0, l=0.0):
    """Calculate the complement of a given value as HSL values.

    :param h: Hue
    :param s: Saturation
    :param l: Lightness
    :return: Complement colour as H, S, L
    """
    return (h + 180) % 360, s, l


def complement_rgb(r=0, g=0, b=0):
    """Convert an RGB colours to its complementary colour.

    :param r: Red
    :param g: Green
    :param b: Blue
    :return: A tuple containing R, G, B colours
    """
    h, s, l = rgb2hsl(r, g, b)
    h, s, l = complement_hsl(h, s, l)
    return hsl2rgb(h, s, l)
