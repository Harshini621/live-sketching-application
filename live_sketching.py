#Importing all the required libraries

import cv2 as cv
import numpy as np
import os

def sketch(image):
    #Converting image to grayscale

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imshow('Original image',image)
    cv.imshow('Gray image', gray)
    
    #cleaning up using gaussian blur

    blur = cv.GaussianBlur(gray,(5,5),0)
    cv.imshow('Original image',image)
    cv.imshow('Blurred', blur)
    
    #extracting edges using canny edge

    edges = cv.Canny(blur,100,200)
    cv.imshow('Original image',image)
    cv.imshow('Edge image', edges)
    
    #threshold inversion

    ret, mask = cv.threshold(edges, 127, 255, cv.THRESH_BINARY_INV)
    cv.imshow('Original image',image)
    cv.imshow('threshold inversion', mask)
    return mask


camera = cv.VideoCapture(0)
if not camera.isOpened():
    print("Cannot open camera")
    exit()
if not os.path.exists('images'):
    os.makedirs('images')
i = 0

while True:
    ret, frame = camera.read()
    if ret == False:
        break
    cv.imshow('livesketcher',sketch(frame))
    name = './images/frame' + str(i) + '.jpg'
    print ('Creating...' + name)
    cv.imwrite(name, sketch(frame))
    i+=1
    key = cv.waitKey(1)
    if key == ord('q'):
        break

cv.destroyAllWindows()
camera.release()