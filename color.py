from PIL import Image
from math import sqrt
import sys
in_file = sys.argv[1]
out_file = sys.argv[2]
old = Image.open(in_file).convert('RGBA')
w, h = old.size
def getOldPixel(x, y):
    return old.getpixel((x, y))
COLORS = (
    (109, 0, 26),
    (255, 69, 0),
    (255, 214, 53),
    (0, 163, 104),
    (126, 237, 86),
    (0, 158, 170),
    (36, 80, 164),
    (81, 233, 244),
    (106, 92, 255),
    (129, 30, 159),
    (228, 171, 255),
    (255, 56, 129),
    (109, 72, 47),
    (255, 180, 112),
    (81, 82, 82),
    (212, 215, 217),
    (190, 0, 57),
    (255, 168, 0),
    (255, 248, 184),
    (0, 204, 120),
    (0, 117, 111),
    (0, 204, 192),
    (54, 144, 234),
    (73, 58, 193),
    (148, 179, 255),
    (180, 74, 192),
    (222, 16, 127),
    (255, 153, 170),
    (156, 105, 38),
    (0, 0, 0),
    (137, 141, 144),
    (255, 255, 255)
)
def closestColor(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]
new = Image.new("RGBA", (w,h));
for i in range(0,w):
    for j in range(0,h):
        r, g, b, a = getOldPixel(i, j)
        if a==0:
            new.putpixel((i, j), (0, 0, 0, 0))
        else:
            r,g,b = closestColor((r, g, b))
            new.putpixel((i, j), (r, g, b, a))
new.save(out_file)
print("    DONE!");
