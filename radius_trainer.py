import numpy as np
from sklearn import svm
from sklearn import ensemble
from json import load
from pickle import dumps
from time import time

center = (1122, 984)

#Makes radius feature from x,y coordinates
def rad_relation(obj_list):
    output = []
    for obj in obj_list:
        x = center[0] - obj[0]
        y = center[1] - obj[1]
        rad = int((x**2 + y**2)**(1/2))
        output.append([rad, obj[2], obj[3], obj[4]])
    return output

#loading all json files into objects
with open("C:\\Users\\JohnVR\\Desktop\\data\\background_data.json", 'r') as ifile:
    background_obj = load(ifile)
with open("C:\\Users\\JohnVR\\Desktop\\data\\black_data.json", 'r') as ifile:
    black_obj = load(ifile)
with open("C:\\Users\\JohnVR\\Desktop\\data\\brown_data.json", 'r') as ifile:
    brown_obj = load(ifile)
with open("C:\\Users\\JohnVR\\Desktop\\data1\\brown.json", 'r') as ifile:
    brown_obj += load(ifile)
with open("C:\\Users\\JohnVR\\Desktop\\data\\shadows_data.json", 'r') as ifile:
    shadows_obj = load(ifile)
with open("C:\\Users\\JohnVR\\Desktop\\data\\white_data.json", 'r') as ifile:
    white_obj = load(ifile)

#Taking about 2000 examples of each object class. 
X = rad_relation(background_obj)[::50]
X += rad_relation(black_obj)[::3]
X += rad_relation(brown_obj)[::8]
X += rad_relation(shadows_obj)[::4]
X += rad_relation(white_obj)[::2]
X = np.array(X)

X_test = rad_relation(background_obj)[1::50]
X_test += rad_relation(black_obj)[1::3]
X_test += rad_relation(brown_obj)[1::8]
X_test += rad_relation(shadows_obj)[1::4]
X_test += rad_relation(white_obj)[1::2]
X_test = np.array(X_test)

#Making target list (np.array)
y = []
for _ in range(0, len(background_obj[::50])):
    y.append(1)
for _ in range(0, len(black_obj[::3])):
    y.append(2)
for _ in range(0, len(brown_obj[::8])):
    y.append(3)
for _ in range(0, len(shadows_obj[::4])):
    y.append(4)
for _ in range(0, len(white_obj[::2])):
    y.append(5)
y = np.array(y)

y_test = []
for _ in range(0, len(background_obj[1::50])):
    y_test.append(1)
for _ in range(0, len(black_obj[1::3])):
    y_test.append(2)
for _ in range(0, len(brown_obj[1::8])):
    y_test.append(3)
for _ in range(0, len(shadows_obj[1::4])):
    y_test.append(4)
for _ in range(0, len(white_obj[1::2])):
    y_test.append(5)
y_test = np.array(y_test)

#Create and train classifier. Dump classifier object into a file
clf = svm.SVC(kernel='linear')
start = time()
clf.fit(X, y)
end = time()
print(clf.score(X_test, y_test))
s = dumps(clf)
with open("C:\\Users\\JohnVR\\Desktop\\data1\\svm_linear4.pkl", 'wb+') as ofile:
    ofile.write(s)
print("Time:", end-start)