import cv2
from numpy import *

imageOrg = cv2.imread("yo.png")
image = cv2.resize(imageOrg,(0,0),fx=0.25,fy=0.25)

imggrey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

image = cv2.bitwise_not(imggrey)
image = cv2.GaussianBlur(image,(21,21),0)

invertedblur = cv2.bitwise_not(image)

image = cv2.divide(imggrey,invertedblur,scale=250)

maxIntensity = 255.0 # depends on dtype of image data
x = arange(maxIntensity) 

# Parameters for manipulating image data
phi = 1
theta = 1

# Increase intensity such that
# dark pixels become much brighter, 
# bright pixels become slightly bright
#newImage0 = (maxIntensity/phi)*(image/(maxIntensity/theta))**0.5
#newImage0 = array(newImage0,dtype=uint8)

#cv2.imshow('newImage0',newImage0)
#cv2.imwrite('newImage0.jpg',newImage0)

y = (maxIntensity/phi)*(x/(maxIntensity/theta))**0.5

# Decrease intensity such that
# dark pixels become much darker, 
# bright pixels become slightly dark 
image = (maxIntensity/phi)*(image/(maxIntensity/theta))**2
image = array(image,dtype=uint8)

cv2.imshow("hello",imageOrg)

cv2.imshow("hello",image)
cv2.waitKey(0)
