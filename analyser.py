from json import dump

def getNeighboursW(pix, x, y, w, h):
    """
    Returns list of white pixle neighbours.
    """
    neighbours = []
    for nx in range(x-1, x+2):
        if nx >= 0 and nx < w:
            for ny in range(y-1, y+2):
                if ny >= 0 and ny < h:
                    if pix[nx, ny] == (0, 255, 0):
                        pix[nx, ny] = (0, 254, 0)
                        neighbours.append((nx, ny))
    return neighbours

def getNeighboursD(pix, x, y, w, h):
    """
    Returns list of dark pixle neighbours.
    """
    neighbours = []
    for nx in range(x-1, x+2):
        if nx >= 0 and nx < w:
            for ny in range(y-1, y+2):
                if ny >= 0 and ny < h:
                    if pix[nx, ny] == (255, 140, 0):
                        pix[nx, ny] = (255, 140, 1)
                        neighbours.append((nx, ny))
                    elif pix[nx, ny] == (0, 0, 0):
                        pix[nx, ny] = (0, 0, 1)
                        neighbours.append((nx, ny))
    return neighbours

def listcords(pairs,i, j):
    """
    Lists all cords of same type i.e. all maxX cords
    """
    result = []
    [result.append(x[i][j]) for x in pairs]
    return result

def merge(pairs):
    """
    Merges list of bounding boxes.
    """
    maxx = max(listcords(pairs, 0, 0))
    minx = min(listcords(pairs, 0, 1))
    maxy = max(listcords(pairs, 1, 0))
    miny = min(listcords(pairs, 1, 1))
    return [[maxx, minx], [maxy, miny]]

def overlapping(list1, list2):
    """
    Return True if bounding boxes overlap.
    """
    return (list1[0][1] <= list2[0][0]) and (list2[0][1] <= list1[0][0]) and (list1[1][1] <= list2[1][0]) and (list2[1][1] <= list1[1][0])

def check(temp, name):
    """
    Checks if bounding boxes are overlapping. Then returns a dictionary of bounding boxes.
    """
    if len(temp) == 0:
        return {}
    elif len(temp) == 1:
        return {name + "1": temp[0]}
    else:
        result = temp
        enddic = {}
        merged = True
        while merged:
            merged = False
            mergelist = []
            removeset = set()
            temp = result
            while len(temp) > 1:
                pairs = [temp[0]]
                for i in range(1, len(temp)):
                    if overlapping(temp[0], temp[i]):
                        pairs.append(temp[i])
                        removeset.add((tuple(temp[0][0]), tuple(temp[0][1])))
                        removeset.add((tuple(temp[i][0]), tuple(temp[i][1])))
                if len(pairs) > 1:
                    mergelist.append(merge(pairs))
                    merged = True
                temp = temp[1:]
            [result.remove(list((list(item[0]), list(item[1])))) for item in removeset]
            [result.append(item) for item in mergelist if item not in result]
        for i, res in enumerate(result):
            enddic[name + str(i+1)] = res
        return enddic

def getBox(temp):
    templist = []
    for particle in temp:
        maxx = max([i[0] for i in particle])
        minx = min([i[0] for i in particle])
        maxy = max([i[1] for i in particle])
        miny = min([i[1] for i in particle])
        templist.append([[maxx, minx], [maxy, miny]])
    return templist

def analyser(iinput, output, scale, pnum, limit, bboxflag):
    """
    Analyses groups of pixels as particles and calculates bounding boxs. Then calculates and returns features. 
    """
    im = iinput
    pix = im.load()
    already = False
    black = []
    brown = []
    white = []
    w = im.width
    h = im.height
    
    #Goes through image looking for colored pixels. First white and then dark particles
    for x in range(0, w):
        for y in range(0, h):
            if pix[x, y] == (0, 255, 0):
                if len(white) < limit:
                    eflag = False
                    #Checks if pixel is part of particle already
                    for sublist in reversed(white):
                        if (x, y) in sublist:
                            eflag = True
                            break
                    #If not, then make new particle and add all neighbouring pixels
                    if not eflag:
                        particle = []
                        i = 0
                        particle.append((x, y))
                        pix[x, y] = (0, 254, 0)
                        while i < len(particle):
                            neighbours = getNeighboursW(pix, particle[i][0], particle[i][1], w, h)
                            [particle.append(cords) for cords in neighbours]
                            i += 1
                        if len(particle) > pnum:
                            white.append(particle)
                else:
                    if not already:
                        print("WARNING: Aquisition capped. More white particles found than the limit.")
                        already = True
            #Same happens for dark pixels.
            elif pix[x, y] == (255, 140, 0) or pix[x, y] == (0, 0, 0):
                eflag = False
                for sublist in reversed(brown):
                    if (x, y) in sublist:
                        eflag = True
                        break
                for sublist in reversed(black):
                    if (x, y) in sublist:
                        eflag = True
                        break
                if not eflag:
                    particle = []
                    i = 0
                    particle.append((x, y))
                    if pix[x, y] == (255, 140, 0):
                        pix[x, y] = (255, 140, 1)
                    elif pix[x, y] == (0, 0, 0):
                        pix[x, y] = (0, 0, 1)
                    while i < len(particle):
                        neighbours = getNeighboursD(pix, particle[i][0], particle[i][1], w, h)
                        [particle.append(cords) for cords in neighbours]
                        i += 1
                    if len(particle) > pnum:
                        blflag = False
                        #If any pixel is black, then the whole particle is black.
                        for cords in particle:
                            if pix[cords[0], cords[1]] == (0, 0, 1):
                                blflag = True
                                break
                        if blflag:
                            black.append(particle)
                        else:
                            brown.append(particle)
    im.close()
    result = []
    
    #Creating bounding boxes for white particles.
    templist = getBox(white)
    whitedic = check(templist, "w_")
    result.append(whitedic)

    #Creating bounding boxes for brown particles.
    templist = getBox(brown)
    browndic = check(templist, "br_")

    #Create bounding boxes for black particles.
    templist = getBox(black)

    #Checks if any brown particles are overlapping with black particles. If so, merge to black and remove from brown.
    lappings = []
    for key in browndic:
        for i,_ in enumerate(templist):
            if overlapping(browndic[key], templist[i]):
                temp = merge([browndic[key], templist[i]])
                lappings.append(key)
                templist[i] = temp
                break
    
    for key in lappings:
        browndic.pop(key, None)

    blackdic = check(templist, "bl_")

    result.append(browndic)
    result.append(blackdic)
    if bboxflag:
        with open(output, "w+") as ofile:
            dump(result, ofile)
    
    #Calculating output features.
    widths = []
    heights = []
    labels = []

    for particles in result:
        for particle in particles:
            widths.append((particles[particle][0][0]*scale)-(particles[particle][0][1]*scale))#Here is where the imprecision comes in. *scale
            heights.append((particles[particle][1][0]*scale)-(particles[particle][1][1]*scale))
            if particle.startswith("w"):
                labels.append(1.0)
            elif particle.startswith("br"):
                labels.append(2.0)
            elif particle.startswith("bl"):
                labels.append(3.0)
    return (widths, heights, labels)