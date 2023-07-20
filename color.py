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
    (107, 0, 25),
    (186, 0, 56),
    (255, 68, 0),
    (255, 167, 0),
    (255, 210, 52),
    (255, 247, 183),
    (0, 163, 104),
    (0, 204, 119),
    (126, 236, 86),
    (0, 116, 110),
    (0, 158, 170),
    (0, 204, 192),
    (36, 80, 164),
    (54, 144, 234),
    (81, 233, 244),
    (73, 58, 193),
    (106, 92, 255),
    (148, 179, 255),
    (129, 30, 159),
    (180, 74, 192),
    (288, 171, 255),
    (222, 16, 127),
    (255, 56, 129),
    (255, 153, 170),
    (109, 72, 47),
    (156, 105, 38),
    (255, 180, 112),
    (0, 0, 0),
    (81, 82, 82),
    (137, 141, 144),
    (212, 215, 217),
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
