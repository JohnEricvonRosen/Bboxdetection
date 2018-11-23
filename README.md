# Bboxdetection
Python 3.6
These programs generate bounding boxes for pictures of particles. 

datagen.py takes creates training data from ImageJ roi annotations. It is important to avoid annotations that have concave shapes. The annotation should not move 'inside' itself.  

radius_trainer.py trains a classifier based on training data. Example classifier is svm_linear.pkl.

svmbboxdetection.py creates a result.res2 and optionaly a color image (-a), a bounding box (-b) annotation from images using an svm classifier. There are many arguments to be parsed and can be seen if you execute the script with a -h tag. There are some prerequisites and assumptions:
1. The program makes predictions for all .bmp images in the directory. Any .bmp files that shouldn't be part of the prediction  shouldn't be removed from the directory. 
2. All images are the same size. The size is important when rescaling the image.
3. Scaling the image results in faster analysis. However the calculations will not be as accurate.
