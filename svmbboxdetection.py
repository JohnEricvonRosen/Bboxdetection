import radius_predictor
import analyser
import bbox
from argparse import ArgumentParser
from sys import exit as iexit
from os import listdir
from PIL.Image import open as iopen
from pickle import loads
from json import dump
import numpy as np

def calcfeat(widths, heights, labels):
    """
    Function calculates standard features and returns them together with particle label and numOfFereteRotationSteps
    """
    numOfElements = len(widths)
    features = {'label': [], 
                'minFeret': [],
                'maxFeret': [],
                'meanFeret': [],
                'aspectRatio': [],
                'numOfFeretRotationSteps':[],
                'area':[],
                'perimeter':[],
                'areaEquivalentDiameter':[],
                'perimeterEquivalentDiameter':[],
                'circularityFormFactor':[],
                'circularity':[],
                }
    # calculate features
    for idx in range(numOfElements):
        w = widths[idx]
        h = heights[idx]
        # label
        features['label'].append(labels[idx])
        # minFeret
        minFeret = min(w,h)
        features['minFeret'].append( minFeret )
        # maxFeret
        maxFeret = np.sqrt(w*w + h*h)
        features['maxFeret'].append( round(maxFeret, 4) )
        # meanFeret
        """
        https://en.wikipedia.org/wiki/Feret_diameter
        From Cauchy's theorem it follows that for a 2D convex body, the Feret diameter averaged over all directions (<F>) 
        is equal to the ratio of the object perimeter (P) and pi, i.e., <F> = P/pi. 
        There is no such relation between <F> and P for a concave object.[1][2]
        """
        perimeter = 2*(w+h)
        meanFeret = perimeter / np.pi 
        features['meanFeret'].append( round(meanFeret, 4) )
        # aspect ratio
        features['aspectRatio'].append( round(minFeret/maxFeret, 4) )
        # number of Feret rotation steps
        features['numOfFeretRotationSteps'].append( 0 ) # numerical calculation of Feret is not necessary
        # area
        area = w*h
        features['area'].append( area )
        # perimeter
        features['perimeter'].append( perimeter )
        # area equivalent diameter
        areaEquivalentDiameter = 2*np.sqrt( area / np.pi )
        features['areaEquivalentDiameter'].append( round(areaEquivalentDiameter, 4) )
        # perimeter equivalent diameter
        perimeterEquivalentDiameter = perimeter / np.pi
        features['perimeterEquivalentDiameter'].append( round(perimeterEquivalentDiameter, 4) )
        # circularity form factor
        circularityFormFactor = 4*np.pi*area / perimeter**2
        features['circularityFormFactor'].append( round(circularityFormFactor, 4) )
        # circularity 
        features['circularity'].append( round(np.sqrt(circularityFormFactor), 4) )

    return features

def main():
    parser = ArgumentParser()
    parser.add_argument("--input", "-i", help="Input image file path.")
    parser.add_argument("--output", "-o", help="Output directory path.")
    parser.add_argument("--classifier", "-c", help="Classifier file path.")
    parser.add_argument("--centerX", "-x", help="X-Coordinate of the center of brightness", type=int)
    parser.add_argument("--centerY", "-y", help="Y-Coordinate of the center of brightness", type=int)
    parser.add_argument("--scale", "-s", help="Downscale the image by a factor of x", type=int)
    parser.add_argument("--remove", "-r", help="How many iterations of noise removal?", type=int)
    parser.add_argument("--neighbours", "-n", help="How many neighbours should be present", type=int)
    parser.add_argument("--pnum", "-p", help="Min number of pixels in particle", type=int)
    parser.add_argument("--limit", "-l", help="Max number of white particles. 0 = unlimited.", type=int)
    parser.add_argument("--anoflag", "-a", help="Should the analysis image be saved?", action="store_true")
    parser.add_argument("--bboxflag", "-b", help="Should the bounding boxes be saved?", action="store_true")
    args = parser.parse_args()

    if args.input:
        iinput = args.input
    else:
        print("Input not provided. Try -h for help.\nexiting...")
        iexit(1)
    if args.output:
        output = args.output
    else:
        print("Output not provided. Try -h for help.\nexiting...")
        iexit(1)
    if args.classifier:
        svm = args.classifier
    else:
        print("Classifier not provided. Try -h for help.\nexiting...")
        iexit(1)
    if args.scale:
        scale = args.scale
    else:
        scale = 1
    if args.centerX:
        centerX = args.centerX
    else:
        print("Center X-Coordinate not provided. Try -h for help.\nexiting...")
        iexit(1)
    if args.centerY:
        centerY = args.centerY
    else:
        print("Center Y-Coordinate not provided. Try -h for help.\nexiting...")
        iexit(1)
    if args.remove:
        murderiter = args.remove
    else:
        print("Removal iterations not provided. Try -h for help.\nexiting...")
        iexit(1)
    if args.neighbours:
        neinum = args.neighbours
    else:
        print("Number of neighbours not provided. Try -h for help.\nexiting...")
        iexit(1)
    if args.pnum:
        pnum = args.pnum
    else:
        pnum = 10
    if args.limit:
        limit = args.limit
    else:
        limit = 10000

    center = (int(centerX/scale), int(centerY/scale))
    
    directory = listdir(iinput)
    files = []
    [files.append((iinput + '\\' + file, output + '\\' + file[:-4] + "_s{0:.2f}".format(1/scale) + '_r' + str(murderiter) + "_n" + str(neinum) + '.jpg', 
                output + '\\' + file[:-4] + '.json', output + '\\' + file[:-4] + '_bbox' + '.jpg')) for file in directory if file.endswith('.bmp')]
    resFile = output + '\\result.res2'

    im = iopen(files[0][0])
    size = (int(im.width/scale), int(im.height/scale))
    im.close()

    #Loads classifier from file
    with open(svm, "rb") as ifile:
        svc = loads(ifile.read())

    widths = []
    heights = []
    labels = []

    for file in files:
        w, h, l = analyser.analyser(radius_predictor.predictor(file[0], svc, file[1], scale, center, murderiter, neinum, size, args.anoflag), file[2], scale, pnum, limit, args.bboxflag)
        widths += w
        heights += h
        labels += l
        if args.bboxflag:
            bbox.bbox(file[0], file[3], file[2], scale, size)

    features = calcfeat(widths, heights, labels)
    result = {"probeId": "probe", "surveyPoint": {"numericMap": {}, "stringMap": {}, "diagramMap": {}}, "particles": {"numericMap": features, "stringMap": {}, "diagramMap": {}}}

    with open(resFile, 'w+') as f:
        dump(result, f)

if __name__ == "__main__":
    main()