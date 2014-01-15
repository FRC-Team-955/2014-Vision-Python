import cv2
import math
from rectangle import Rectangle

camera = cv2.VideoCapture(1)
foundHotTarget = False
viewAngleVert = 18.2
resHalfY = 240
horizTarget = Rectangle(0.0, 0.0, 23.5, 4.0)
vertTarget = Rectangle(0.0, 0.0, 4.0, 32.0)

cv2.namedWindow('robot threshold', cv2.WINDOW_NORMAL)
cv2.namedWindow('robot processed', cv2.WINDOW_NORMAL)
cv2.namedWindow("robot binary", cv2.WINDOW_NORMAL)

print "vision name", __name__

def update():
    print "update()"

    # Get color image from camera
    ret, img = camera.read() # img.shape 640x480 image

    # Convert color image to grayscale image
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("robot processed",grayImg)
    cv2.waitKey(10)
    
    # Convert grayscale image to binary image, 0 = black, 255 = white
    # cv2.threshold(img, thresh, newVal, mode)
    #ret, binaryImg = cv2.threshold(grayImg, 150, 255, cv2.THRESH_BINARY)
    binaryImg = cv2.adaptiveThreshold(grayImg, 
                                          maxValue=200, 
                                          #adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                          thresholdType=cv2.THRESH_BINARY,
                                          blockSize=7,
                                          C=-5)
    # cv2.Canny(img, minThresh, maxThresh)
    cv2.imshow("robot binary", binaryImg)
    #binaryImg = cv2.Canny(binaryImg, 100, 200)
    cv2.imshow("robot threshold",binaryImg)
    cv2.waitKey(10)

    # Find all contours, counter is vector of points that are connected to make up a shape
    # cv2.findCountors(binaryImg, mode, method)
    contours, hierarchy = cv2.findContours(binaryImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Parse contours, calculate distance and check if it's the hot target
    for shape in contours:

        approx = cv2.approxPolyDP(shape, cv2.arcLength(shape, True) * 0.2, True) 
        if len(approx) != 4:
            continue
        target = Rectangle(*approx)
        
        # Filter out noise
        if target.width < 50 or target.width > 300 or target.height < 50 or target.height > 300:
            continue
        foundHotTarget = False
        realHeight = vertTarget.height
        print target.printSelf()
        # If the width of the target is greater than its height then it's probably the hot target
        if target.width > target.height * 2.5:
            realHeight = horizTarget.height
            #drawRect(grayImg, target)
            foundHotTarget = True
            drawRect(grayImg, target)
            distance = computDistance(realHeight, target.height)
            viewAngle = computeAngle(realHeight, target.height, 11)
            print "Distance: ", round(distance), "Veiw Angle: ", viewAngle, " Hot Target: ", foundHotTarget
    cv2.imshow("robot processed",grayImg)
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