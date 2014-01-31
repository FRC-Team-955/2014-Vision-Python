import cv2
import math
import numpy as np
from rectangle import Rectangle

camera = cv2.VideoCapture(1)
foundHotTarget = False
foundHorzTarget = False
viewAngleVert = 19.832 
resHalfY = 240
horizTarget = Rectangle(0.0, 0.0, 23.5, 4.0)
vertTarget = Rectangle(0.0, 0.0, 4.0, 32.0)
debugMode = False

if debugMode:
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.namedWindow('filtered', cv2.WINDOW_NORMAL)

print "vision name", __name__

def update():
    print "update()"

    # Get color image from camera
    ret, img = camera.read() # img.shape 640x480 image

    # Convert to hsv img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Keep only green objects
    # higher s = less white, higher v = less black
    lowerGreen = np.array([70, 70, 180])
    upperGreen = np.array([110, 130,255])
    filteredGreen = cv2.inRange(hsv, lowerGreen, upperGreen)

    # Filter out small objects
    filteredGreen = cv2.morphologyEx(filteredGreen, cv2.MORPH_OPEN, np.ones((3, 3)))

    # Find all contours, counter is vector of points that are connected to make up a shape
    contours, hierarchy = cv2.findContours(filteredGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Resetting values
    foundHotTarget = False;
    foundHorzTarget = False

    # Parse contours, calculate distance and check if it's the hot target
    for shape in contours:
        target = Rectangle(*cv2.boundingRect(shape))

        # Filter out small contours
        if target.getArea() > 300 and target.getArea() < 10000:

            # If the width of the target is greater than its height then it's probably the hot target
            if target.width >= target.height * 2.5:
                foundHotTarget = True
                distance = computeDistance(horizTarget.height, target.height)
                
                if debugMode:
                    drawRect(img, target)
                    viewAngle = computeAngle(horizTarget.height, target.height, 228)
                    print "Distance: ", round(distance), ", Hot Target", viewAngle, viewAngleVert

            # If the height of the target is greater than the its width its probably a vert target
            elif target.height >= target.width * 6:
                foundHorzTarget = True
                distance = computeDistance(vertTarget.height, target.height)

                if debugMode:
                    drawRect(img, target)
                    viewAngle = computeAngle(vertTarget.height, target.height, 228)
                    print "Distance: ", round(distance), ", Vert Target", viewAngle, viewAngleVert
    
    if debugMode:
        cv2.imshow("color", img)
        cv2.waitKey(10)
        cv2.imshow("filtered", filteredGreen)
        cv2.waitKey(10)

def computeDistance(realHeight, targetHeight):
    return ((realHeight / targetHeight) * resHalfY) / math.tan(viewAngleVert * math.pi / 180.0)

def computeAngle(realHeight, targetHeight, distance):
    return math.atan(((realHeight / targetHeight) * resHalfY) / distance) * 180.0 / math.pi

def drawRect(img, rect):
    cv2.rectangle(img, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), 177, 2)

def round(value):
    return math.floor((value * 100) + 0.5) / 100