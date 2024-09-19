import numpy as np
import cv2
import csv
import os
import matplotlib
from skimage.feature import hog

def convert2Hog(data):
    orient = 10
    pixPerCell = 8
    cellsPerBlock = 4

    ans = np.zeros((data.shape[0], 160), float)
    for i in range(data.shape[0]):

        if i % 1000 == 0:
            print(f'converting to HOG: {i}/{data.shape[0]}')

        gray = cv2.cvtColor(data[i], cv2.COLOR_BGR2GRAY)

        normalised_blocks, _ =  hog(gray, 
                                    orientations=orient, 
                                    pixels_per_cell=(pixPerCell, pixPerCell), 
                                    cells_per_block=(cellsPerBlock, cellsPerBlock), 
                                    block_norm='L2-Hys',
                                    transform_sqrt=True,
                                    feature_vector=True,
                                    visualize=True)
        ans[i] = normalised_blocks
    
    return ans


def convert2Hsv(data):
    ans = np.zeros((data.shape[0], 30), float)
    for i in range(data.shape[0]):
        if i % 1000 == 0:
            print(f'converting to HSV: {i}/{data.shape[0]}')
        
        bins = np.linspace(0, 255, 10 + 1)
        hsv = matplotlib.colors.rgb_to_hsv(data[i] / 255) * 255

        imhist, bin_edges = np.histogram(hsv[:, :, 0], bins=bins, density=True)
        hsv_feature = imhist * np.diff(bin_edges)

        imhist, bin_edges = np.histogram(hsv[:, :, 1], bins=bins, density=True)
        imhist = imhist * np.diff(bin_edges)
        hsv_feature = np.hstack((hsv_feature, imhist))

        imhist, bin_edges = np.histogram(hsv[:, :, 2], bins=bins, density=True)
        imhist = imhist * np.diff(bin_edges)
        hsv_feature = np.hstack((hsv_feature, imhist))

        ans[i] = hsv_feature

    return ans
    
def load(filename):
    data_list = []
    with open(filename, "r") as csvf:
        reader = csv.reader(csvf)
        for line in reader:
            data_list.append(line)
    data = np.array(data_list)

    return data

def get_feature(x_train, x_test):
    if not os.path.isfile('./feature/x_train_hog.csv'):
        print('--- train_hog not existed, start converting ---')
        x_train_hog = convert2Hog(x_train)
        np.savetxt( "./feature/x_train_hog.csv", x_train_hog, delimiter=",")
    else:
        print('train_hog existed, read from file')
        x_train_hog = load('./feature/x_train_hog.csv')

    if not os.path.isfile('./feature/x_test_hog.csv'):
        print('--- test_hog not existed, start converting ---')
        x_test_hog = convert2Hog(x_test)
        np.savetxt( "./feature/x_test_hog.csv", x_test_hog, delimiter=",")
    else:
        print('test_hog existed, read from file')
        x_test_hog = load('./feature/x_test_hog.csv')

    if not os.path.isfile('./feature/x_train_hsv.csv'):
        print('--- train_hsv not existed, start converting ---')
        x_train_hsv = convert2Hsv(x_train)
        np.savetxt( "./feature/x_train_hsv.csv", x_train_hsv, delimiter=",")
    else:
        print('train_hsv existed, read from file')
        x_train_hsv = load('./feature/x_train_hsv.csv')

    if not os.path.isfile('./feature/x_test_hsv.csv'):
        print('--- test_hsv not existed, start converting ---')
        x_test_hsv = convert2Hsv(x_test)
        np.savetxt( "./feature/x_test_hsv.csv", x_test_hsv, delimiter=",")
    else:
        print('test_hsv existed, read from file')
        x_test_hsv = load('./feature/x_test_hsv.csv')

    x_train_feature = np.hstack((x_train_hog, x_train_hsv))
    x_test_feature = np.hstack((x_test_hog, x_test_hsv))
    return x_train_feature, x_test_feature
