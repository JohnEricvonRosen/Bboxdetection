from json import load
from PIL.ImageDraw import Draw
from PIL.Image import open as iopen

def bbox(iinput, output, source, scale, size):
    color = [(0, 255, 0, 255), (0, 0, 255, 255), (255, 0, 0, 255)]
    with open(source, "r") as ifile:
        result = load(ifile)

    im = iopen(iinput)
    im = im.resize(size)
    draw = Draw(im)

    for plist in result:
        for key in plist:
            x, y = plist[key]
            x1, x0 = x
            y1, y0 = y
            cords = [(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)]
            if key.startswith('w'):
                pcolor = color[0]
            elif key.startswith('br'):
                pcolor = color[1]
            else:
                pcolor = color[2]
            draw.line(cords, fill=pcolor, width=1)
    del draw
    im.save(output, 'JPEG')
    im.close()