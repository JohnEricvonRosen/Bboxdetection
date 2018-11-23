from read_roi import read_roi_zip
from PIL import Image
import json
#Takes freehand annotations and stores them in a json file.
rois = read_roi_zip("C:\\Users\\JohnVR\\Desktop\\data1\\white1.zip")

newcords = []
for anno in rois:
	cords = list(zip(rois[anno]['x'], rois[anno]['y']))
	cords.sort(key=lambda x: x[1])
	maxx, ly = cords[0]
	minx = maxx
	for cord in cords:
		if cord[1] == ly:
			if cord[0] < minx:
				minx = cord[0]
			elif cord[0] > maxx:
				maxx = cord[0]
		else:
			for i in range(minx, maxx):
				if (i, ly) not in cords: #if there is a point between two x coordinates
					newcords.append((i, ly))#then add them to the list of points
			maxx, ly = cord
			minx = maxx
cords = cords + newcords
cords.sort(key=lambda x: x[1])
img = Image.open("C:\\Users\\JohnVR\\Desktop\\000_00020.bmp")
pix = img.load()

#Data consists of x, y coordinates and r, g, b values
colors = []
for cord in cords:
	r, g, b = pix[cord[0], cord[1]]
	colors.append([cord[0], cord[1], r, g, b])
print(len(colors))
with open("C:\\Users\\JohnVR\\Desktop\\data1\\white.json", 'w+') as hello:
	json.dump(colors, hello)
		