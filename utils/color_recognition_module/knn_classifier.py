#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------
#@ONLINE{vdtct,
#    author = "Ahmet Özlü",
#    title  = "Vehicle Detection, Tracking and Counting by TensorFlow",
#    year   = "2018",
#    url    = "https://github.com/ahmetozlu/vehicle_counting_tensorflow"
#}

import csv
import random
import math
import operator
import cv2

def calculateManhattanDistance(variable1,variable2,length):
    distance = 0
    for i in range(length):
        distance += abs(variable1[i] - variable2[i])
    return distance
# calculation of euclidead distance
def calculateEuclideanDistance(variable1, variable2, length):
    distance = 0
    for i in range(length):
        distance += pow(variable1[i] - variable2[i], 2)
    return math.sqrt(distance)


# get k nearest neigbors
def kNearestNeighbors(training_feature_vector, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for i in range(len(training_feature_vector)):
        dist = calculateManhattanDistance(testInstance, training_feature_vector[i], length)
        #print(testInstance,'|',training_feature_vector[x])
        distances.append((training_feature_vector[i], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors


# votes of neighbors
def responseOfNeighbors(neighbors):
    all_possible_neighbors = {}
    for i in range(len(neighbors)):
        response = neighbors[i][-1]
        if response in all_possible_neighbors:
            all_possible_neighbors[response] += 1
        else:
            all_possible_neighbors[response] = 1
    sortedVotes = sorted(all_possible_neighbors.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0]


# Load image feature data to training feature vectors and test feature vector
def loadDataset(
    filename,
    filename2,
    training_feature_vector=[],
    test_feature_vector=[],
    ):
    with open(filename) as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)):
            for y in range(3):
                dataset[x][y] = float(dataset[x][y])
            training_feature_vector.append(dataset[x])

    with open(filename2) as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)):
            for y in range(3):
                dataset[x][y] = float(dataset[x][y])
            test_feature_vector.append(dataset[x])


def main(training_data, test_data):
    training_feature_vector = []  # training feature vector
    test_feature_vector = []  # test feature vector
    loadDataset(training_data, test_data, training_feature_vector, test_feature_vector)
    classifier_prediction = []  # predictions
    k = 3  # K value of k nearest neighbor
    for i in range(len(test_feature_vector)):
        neighbors = kNearestNeighbors(training_feature_vector, test_feature_vector[i], k)
        result = responseOfNeighbors(neighbors)
        classifier_prediction.append(result)
    return classifier_prediction[0][0]
