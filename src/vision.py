import cv2
import math
from rectangle import Rectangle
import numpy as np

camera = cv2.VideoCapture(0)
foundHotTarget = False
viewAngleVert = 18.87 #37.5
resHalfY = 240
horizTarget = Rectangle(0.0, 0.0, 23.5, 4.0)
vertTarget = Rectangle(0.0, 0.0, 4.0, 32.0)

cv2.namedWindow('hsv', cv2.WINDOW_NORMAL)
cv2.namedWindow('filtered', cv2.WINDOW_NORMAL)

print "vision name", __name__

def update():
    print "update()"

    # Get color image from camera
    ret, img = camera.read() # img.shape 640x480 image

    # Convert to hsv img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv", hsv)
    cv2.waitKey(10)

    # Keep only green objects
    lowerGreen = np.array([90, 0, 200])
    upperGreen = np.array([120, 255,255])
    filteredGreen = cv2.inRange(hsv, lowerGreen, upperGreen)
    cv2.imshow("filtered", filteredGreen)
    cv2.waitKey(10)

    # Find all contours, counter is vector of points that are connected to make up a shape
    contours, hierarchy = cv2.findContours(filteredGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Parse contours, calculate distance and check if it's the hot target
    for shape in contours:
        target = Rectangle(*cv2.boundingRect(shape))
        foundHotTarget = False
        
        # If the width of the target is greater than its height then it's probably the hot target
        if target.width > target.height * 2.5:
            foundHotTarget = True
            drawRect(hsv, target)
            distance = computDistance(horizTarget.height, target.height)
            print "Distance: ", round(distance), " Hot Target: ", foundHotTarget
    cv2.imshow("hsv", hsv)
    cv2.waitKey(10)

def computDistance(realHeight, targetHeight):
    return ((realHeight / targetHeight) * resHalfY) / math.tan(viewAngleVert * math.pi / 180)

def computeAngle(realHeight, targetHeight, distance):
    return math.atan(((realHeight / targetHeight) * resHalfY) / distance) * 180 / math.pi

def drawRect(img, rect):
    cv2.rectangle(img, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), 177, 2)

def round(value):
    return math.floor((value * 100) + 0.5) / 100