import colorsys
import math


class Color:
    def __init__(self, red, green, blue):
        self._bytes = [_clamp(red), _clamp(green), _clamp(blue)]

    @property
    def raw(self):
        return self._bytes



    def __repr__(self):
        return "Color(%s)" % self._bytes


def _clamp(value):
    return min(255, max(0, int(value)))


def from_hsv(hue, saturation, value):
    red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
    return Color(red, green, blue)


def from_kelvin(kelvin, brightness):
    red, green, blue = convert_kelvin_to_rgb(kelvin)
    return Color(red * brightness, green * brightness, blue * brightness)


def convert_kelvin_to_rgb(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    #range check
    if colour_temperature < 1000:
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000

    tmp_internal = colour_temperature / 100.0

    # red
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red

    # green
    if tmp_internal <=66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green

    # blue
    if tmp_internal >=66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue

    return red, green, blue


def wheel(infinite=True):
    while True:
        for p in range(128 * 3 + 1):
            x = 127 - p % 128
            y = p % 128

            if p < 128:
                yield Color(x, y, 0)
            elif p < 256:
                yield Color(0, x, y)
            else:
                yield Color(y, 0, x)

        if not infinite:
            return


AliceBlue = Color(240, 248, 255)
Amethyst = Color(153, 102, 204)
AntiqueWhite = Color(250, 235, 215)
Aqua = Color(0, 255, 255)
Aquamarine = Color(127, 255, 212)
Azure = Color(240, 255, 255)
Beige = Color(245, 245, 220)
Bisque = Color(255, 228, 196)
Black = Color(0, 0, 0)
BlanchedAlmond = Color(255, 235, 205)
Blue = Color(0, 0, 255)
BlueViolet = Color(138, 43, 226)
Brown = Color(165, 42, 42)
BurlyWood = Color(222, 184, 135)
CadetBlue = Color(95, 158, 160)
Chartreuse = Color(127, 255, 0)
Chocolate = Color(210, 105, 30)
Coral = Color(255, 127, 80)
CornflowerBlue = Color(100, 149, 237)
Cornsilk = Color(255, 248, 220)
Crimson = Color(220, 20, 60)
Cyan = Color(0, 255, 255)
DarkBlue = Color(0, 0, 139)
DarkCyan = Color(0, 139, 139)
DarkGoldenrod = Color(184, 134, 11)
DarkGray = Color(169, 169, 169)
DarkGreen = Color(0, 100, 0)
DarkKhaki = Color(189, 183, 107)
DarkMagenta = Color(139, 0, 139)
DarkOliveGreen = Color(85, 107, 47)
DarkOrange = Color(255, 140, 0)
DarkOrchid = Color(153, 50, 204)
DarkRed = Color(139, 0, 0)
DarkSalmon = Color(233, 150, 122)
DarkSeaGreen = Color(143, 188, 143)
DarkSlateBlue = Color(72, 61, 139)
DarkSlateGray = Color(47, 79, 79)
DarkTurquoise = Color(0, 206, 209)
DarkViolet = Color(148, 0, 211)
DeepPink = Color(255, 20, 147)
DeepSkyBlue = Color(0, 191, 255)
DimGray = Color(105, 105, 105)
DodgerBlue = Color(30, 144, 255)
FireBrick = Color(178, 34, 34)
FloralWhite = Color(255, 250, 240)
ForestGreen = Color(34, 139, 34)
Fuchsia = Color(255, 0, 255)
Gainsboro = Color(220, 220, 220)
GhostWhite = Color(248, 248, 255)
Gold = Color(255, 215, 0)
Goldenrod = Color(218, 165, 32)
Gray = Color(128, 128, 128)
Green = Color(0, 255, 0)
GreenYellow = Color(173, 255, 47)
Green_HTML = Color(0, 128, 0)
Honeydew = Color(240, 255, 240)
HotPink = Color(255, 105, 180)
IndianRed = Color(205, 92, 92)
Indigo = Color(75, 0, 130)
Ivory = Color(255, 255, 240)
Khaki = Color(240, 230, 140)
Lavender = Color(230, 230, 250)
LavenderBlush = Color(255, 240, 245)
LawnGreen = Color(124, 252, 0)
LemonChiffon = Color(255, 250, 205)
LightBlue = Color(173, 216, 230)
LightCoral = Color(240, 128, 128)
LightCyan = Color(224, 255, 255)
LightGoldenrodYellow = Color(250, 250, 210)
LightGreen = Color(144, 238, 144)
LightGrey = Color(211, 211, 211)
LightPink = Color(255, 182, 193)
LightSalmon = Color(255, 160, 122)
LightSeaGreen = Color(32, 178, 170)
LightSkyBlue = Color(135, 206, 250)
LightSlateGray = Color(119, 136, 153)
LightSteelBlue = Color(176, 196, 222)
LightYellow = Color(255, 255, 224)
Lime = Color(0, 255, 0)
LimeGreen = Color(50, 205, 50)
Linen = Color(250, 240, 230)
Magenta = Color(255, 0, 255)
Maroon = Color(128, 0, 0)
MediumAquamarine = Color(102, 205, 170)
MediumBlue = Color(0, 0, 205)
MediumOrchid = Color(186, 85, 211)
MediumPurple = Color(147, 112, 219)
MediumSeaGreen = Color(60, 179, 113)
MediumSlateBlue = Color(123, 104, 238)
MediumSpringGreen = Color(0, 250, 154)
MediumTurquoise = Color(72, 209, 204)
MediumVioletRed = Color(199, 21, 133)
MidnightBlue = Color(25, 25, 112)
MintCream = Color(245, 255, 250)
MistyRose = Color(255, 228, 225)
Moccasin = Color(255, 228, 181)
NavajoWhite = Color(255, 222, 173)
Navy = Color(0, 0, 128)
Off = Color(0, 0, 0)
OldLace = Color(253, 245, 230)
Olive = Color(128, 128, 0)
OliveDrab = Color(107, 142, 35)
On = Color(255, 255, 255)
Orange = Color(255, 165, 0)
OrangeRed = Color(255, 69, 0)
Orchid = Color(218, 112, 214)
PaleGoldenrod = Color(238, 232, 170)
PaleGreen = Color(152, 251, 152)
PaleTurquoise = Color(175, 238, 238)
PaleVioletRed = Color(219, 112, 147)
PapayaWhip = Color(255, 239, 213)
PeachPuff = Color(255, 218, 185)
Peru = Color(205, 133, 63)
Pink = Color(255, 192, 203)
Plaid = Color(204, 85, 51)
Plum = Color(221, 160, 221)
PowderBlue = Color(176, 224, 230)
Purple = Color(128, 0, 128)
Red = Color(255, 0, 0)
RosyBrown = Color(188, 143, 143)
RoyalBlue = Color(65, 105, 225)
SaddleBrown = Color(139, 69, 19)
Salmon = Color(250, 128, 114)
SandyBrown = Color(244, 164, 96)
SeaGreen = Color(46, 139, 87)
Seashell = Color(255, 245, 238)
Sienna = Color(160, 82, 45)
Silver = Color(192, 192, 192)
SkyBlue = Color(135, 206, 235)
SlateBlue = Color(106, 90, 205)
SlateGray = Color(112, 128, 144)
Snow = Color(255, 250, 250)
SpringGreen = Color(0, 255, 127)
SteelBlue = Color(70, 130, 180)
Tan = Color(210, 180, 140)
Teal = Color(0, 128, 128)
Thistle = Color(216, 191, 216)
Tomato = Color(255, 99, 71)
Turquoise = Color(64, 224, 208)
Violet = Color(238, 130, 238)
Wheat = Color(245, 222, 179)
White = Color(255, 255, 255)
WhiteSmoke = Color(245, 245, 245)
Yellow = Color(255, 255, 0)
YellowGreen = Color(154, 205, 50)
