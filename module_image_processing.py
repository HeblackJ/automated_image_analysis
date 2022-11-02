## Definitions for image processing & filtering  ##

import cv2
import matplotlib.pyplot as plt
import numpy as np

# change image colour format (RGB, HSV, grey-scale)
def rgb2hsv(image):
 hsv_img = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
 return (hsv_img)

def rgb2grey(image):
 grayimg = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
 return (grayimg)

# denoising of image
def denoise(img):
	denoised=cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
	return (denoised)

# saving of images --> saving directory has to be stated under "name"
def saveimagejpeg(image,name="unknown"):
 cv2.imwrite(name+'.jpeg', image)

# green colour filtering
def maskhsvdenoise_green(img):
	
	denoised=denoise(img)
	hsv = rgb2hsv(denoised)

	lower_green = np.array([32,50,25])
	upper_green = np.array([100,255,180])
	mask = cv2.inRange(hsv, lower_green, upper_green)
	result_green = cv2.bitwise_and(img, img, mask=mask)

	return(result_green)

# red colour filtering
def maskhsvdenoise_red(img):
	denoised = denoise(img)
	hsv = rgb2hsv(denoised)

	lower_red = np.array([136, 15, 36])
	upper_red = np.array([180, 255, 245])
	mask = cv2.inRange(hsv, lower_red, upper_red)
	result_red = cv2.bitwise_and(img, img, mask=mask)

	# additional blurring step for red colour filtering (15x15 matrix around specific pixel need to be in the red colour range to be assigned to it --> removes soil artifacts)
	kernel = np.ones((15, 15), np.float32) / 225
	result_red = cv2.filter2D(result_red, -1, kernel)

	return (result_red)

# read information from file (tab-wise)
def readtabtable(filename):
	table=open( filename,"r")
	cleanedtable=[x.replace("\n","").split("\t") for x in table]
	return cleanedtable