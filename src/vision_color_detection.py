import cv2
import math
from rectangle import Rectangle
import numpy as np

camera = cv2.VideoCapture(1)
foundHotTarget = False
viewAngleVert = 37.5 #18.2
resHalfY = 240
horizTarget = Rectangle(0.0, 0.0, 23.5, 4.0)
vertTarget = Rectangle(0.0, 0.0, 4.0, 32.0)
index = 0

cv2.namedWindow('color', cv2.WINDOW_NORMAL)
cv2.namedWindow('filtered', cv2.WINDOW_NORMAL)

print "vision name", __name__

def update():
    print "update() 2"

    # Get color image from camera
    ret, img = camera.read() # img.shape 640x480 image

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    global index
    index += 1
    #cv2.imwrite("hsv" + str(index) + ".jpg", hsv)
    cv2.imshow("color", hsv)
    cv2.waitKey(10)

    # 105, 137, 230, 255, 133, 183
    # lowerGreen = np.array((100, 20, 100))
    # upperGreen = np.array((170, 100, 170))
    lowerGreen = np.array([0, 100, 255], np.uint8)
    upperGreen = np.array([9, 200, 255], np.uint8)

    filteredGreen = cv2.inRange(hsv, lowerGreen, upperGreen)
    cv2.imshow("filtered", filteredGreen)
    cv2.waitKey(10)
    

    # Find all contours, counter is vector of points that are connected to make up a shape
    # cv2.findCountors(img, mode, method)
    contours, hierarchy = cv2.findContours(filteredGreen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Parse contours, calculate distance and check if it's the hot target
    for shape in contours:
        approx = cv2.approxPolyDP(shape, cv2.arcLength(shape, True) * 0.2, True) 
        cv2.drawContours(hsv,[approx],0, np.random.randint(0,255,(3)).tolist(), 2)
        if len(approx) != 4:
            continue
        target = Rectangle(*approx)
        print target.printSelf
        # Filter out noise
        if target.width < 50 or target.width > 300 or target.height < 50 or target.height > 300:
            continue
        foundHotTarget = False
        realHeight = vertTarget.height
        # If the width of the target is greater than its height then it's probably the hot target
        if target.width > target.height * 2.5:
            realHeight = horizTarget.height
            #drawRect(grayImg, target)
            foundHotTarget = True
        drawRect(hsv, target)
        distance = computDistance(realHeight, target.height)
        viewAngle = computeAngle(realHeight, target.height, 11)
        print "Distance: ", round(distance), "Veiw Angle: ", viewAngle, " Hot Target: ", foundHotTarget
    cv2.imshow("color", hsv)
    cv2.waitKey(10)

def foundHotTarget():
    return foundHotTarget

def computDistance(realHeight, targetHeight):
    return ((realHeight / targetHeight) * resHalfY) / math.tan(viewAngleVert * math.pi / 180)

def computeAngle(realHeight, targetHeight, distance):
    return math.atan(((realHeight / targetHeight) * resHalfY) / distance) * 180 / math.pi

def drawRect(img, rect):
    #cv2.rectangle(img, pt1, pt2, color, thickness)
    cv2.rectangle(img, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), 177, 2)

def round(value):
    return math.floor((value * 100) + 0.5) / 100