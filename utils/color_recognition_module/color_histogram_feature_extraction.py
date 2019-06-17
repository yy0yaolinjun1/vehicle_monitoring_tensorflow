#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------
#@ONLINE{vdtct,
#    author = "Ahmet Özlü",
#    title  = "Vehicle Detection, Tracking and Counting by TensorFlow",
#    year   = "2018",
#    url    = "https://github.com/ahmetozlu/vehicle_counting_tensorflow"
#}
from PIL import Image
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import itemfreq
from utils.color_recognition_module import knn_classifier as knn_classifier
current_path = os.getcwd()


def color_histogram_of_test_image(test_src_image):

    # load the image
    image = test_src_image

    chans = cv2.split(image)
    colors = ('b', 'g', 'r')
    features = []
    feature_data = ''
    counter = 0
    for (chan, color) in zip(chans, colors):
        counter = counter + 1
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])                                             
        #print(hist)
        features.extend(hist)
 
        # find the peak pixel values for R, G, and B
        elem = np.argmax(hist)
        #print(elem)
        if counter == 1:
            blue = str(elem)
        elif counter == 2:
            green = str(elem)
        elif counter == 3:
            red = str(elem)
            feature_data = red + ',' + green + ',' + blue
    with open(current_path + '/utils/color_recognition_module/'
              + 'test.data', 'w') as myfile:
        myfile.write(feature_data)


def color_histogram_of_training_image(img_name):
    if 'red' in img_name:
        data_source = 'red'
    elif 'yellow' in img_name:
        data_source = 'yellow'
    elif 'green' in img_name:
        data_source = 'green'
    elif 'black' in img_name:
        data_source = 'black'
    # load the image
    image = cv2.imread(img_name)
    chans = cv2.split(image)
    colors = ('b', 'g', 'r')
    features = []
    feature_data = ''
    counter = 0
    for (chan, color) in zip(chans, colors):
        counter = counter + 1

        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)
        elem = np.argmax(hist)

        if counter == 1:
            blue = str(elem)
        elif counter == 2:
            green = str(elem)
        elif counter == 3:
            red = str(elem)
            feature_data = red + ',' + green + ',' + blue

    with open('training.data', 'a') as myfile:
        myfile.write(feature_data + ',' + data_source + '\n')


def training():
    # red color training images
    for f in os.listdir('./training_dataset/red'):
        color_histogram_of_training_image('./training_dataset/red/' + f)

    # yellow color training images
    for f in os.listdir('./training_dataset/yellow'):
        color_histogram_of_training_image('./training_dataset/yellow/' + f)

    # green color training images
    for f in os.listdir('./training_dataset/green'):
        color_histogram_of_training_image('./training_dataset/green/' + f)


    # black color training images
    for f in os.listdir('./training_dataset/black'):
        color_histogram_of_training_image('./training_dataset/black/' + f)

