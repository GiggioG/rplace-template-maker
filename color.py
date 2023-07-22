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
    (255,69,0),
    (255,168,0),
    (255,214,53),
    (0,163,104),
    (126,237,86),
    (36,80,164),
    (54,144,234),
    (81,233,244),
    (129,30,159),
    (180,74,192),
    (255,153,170),
    (156,105,38),
    (0,0,0),
    (137,141,144),
    (212,215,217),
    (255,255,255)
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
