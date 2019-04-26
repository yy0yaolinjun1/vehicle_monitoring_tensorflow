#!/usr/bin/python
#@ONLINE{vdtct,
#    author = "Ahmet Özlü",
#    title  = "Vehicle Detection, Tracking and Counting by TensorFlow",
#    year   = "2018",
#    url    = "https://github.com/ahmetozlu/vehicle_counting_tensorflow"
#}

def crop_center(img,cropx,cropy): # to crop and get the center of the given image
    y,x, channels = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)  
  
    return img[starty:starty+cropy,startx:startx+cropx]
