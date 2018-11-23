from sklearn.svm import SVC
from PIL.Image import open as iopen

def predictor(iinput, svc, output, scale, center, murderiter, neinum, size, anoflag):
    #Per row, make a classification prediction for each pixel.
    im = iopen(iinput)
    im = im.resize(size)
    pix = im.load()
    w = im.width
    h = im.height
    for x in range(0, w):
        args = []
        for y in range(0, h):
            r, g, b = pix[x, y]
            rad = int(((center[0]-x)**2 + (center[1]-y)**2)**(1/2)) * scale
            args.append([rad, r, g, b])
        result = svc.predict(args)

        #Color pixels based on prediction.
        for z, _ in enumerate(args):
            if result[z] == 1: 
                pix[x, z] = (255, 255, 255) # background dart
            elif result[z] == 2:
                pix[x, z] = (0, 0, 0) # black particles
            elif result[z] == 3:
                pix[x, z] = (255, 140, 0) # brown particles
            elif result[z] == 4:
                pix[x, z] = (75, 0, 130) # shadows
            elif result[z] == 5:
                pix[x, z] = (0, 255, 0) # white particles
    for _ in range(0,murderiter):
        murderlist = []
        for x in range(0, w):
            for y in range(0, h):
                neighbours = 0
                if pix[x, y] == (0, 255, 0):
                    for nx in range(x-1, x+2):
                        if nx >= 0 and nx < w:
                            for ny in range(y-1, y+2):
                                if ny >= 0 and ny < h:
                                    if pix[nx, ny] == (0, 255, 0) and (nx, ny) != (x, y):
                                        neighbours += 1
                    if neighbours < neinum:
                        murderlist.append((x, y))
                if pix[x, y] == (75, 0, 130):
                    for nx in range(x-1, x+2):
                        if nx >= 0 and nx < w:
                            for ny in range(y-1, y+2):
                                if ny >= 0 and ny < h:
                                    if pix[nx, ny] == (75, 0, 130) and (nx, ny) != (x, y):
                                        neighbours += 1
                    if neighbours < neinum:
                        murderlist.append((x, y))
        for death in murderlist:
            pix[death[0], death[1]] = (255, 255, 255)
    if anoflag:
        im.save(output, 'JPEG')
    return im