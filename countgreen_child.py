## Here images will be filtered (colour ranges can be found in "module_image_processing.py"), merged, masked, grey-scaled & counted ##

from module_image_processing import *
import time
import os
import numpy as np
import cv2
import sys

## Find out which file to work on

fil=sys.argv[2]
outfolder=sys.argv[3]

qpnum=sys.argv[1]

photoname=fil.split(".")[0].split("/")[-1]

## Get file info
print('getting file information...')
(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(outfolder+"\\"+fil)
mytime=time.ctime(mtime)
mytime=mytime.replace("  "," ").split(" ")
timestring="2021"+"-"+mytime[1]+"-"+mytime[2]  # year has to be adapted manually

## Read file
print('segmenting...')

img = cv2.imread(outfolder+"\\"+fil)

date = photoname.split("-")[0]

## Colour filtering & merging --> refers to module_image_processing where filtering settings & definitions can be found
# colour change of leaves started during the experiment --> to reduce storage amounts red colour filtering is added, when first red leaves occured

if date >= "201130":
    # green pixel filtering & if wanted resulting image can be stored (outcommented)
    maskedhsv_denoised_green = maskhsvdenoise_green(img)
    im_green = maskedhsv_denoised_green
    print "segmented image green: ", fil
    #saveimagejpeg(image=im_green, name=outfolder+"/segmented/"+photoname+"_green")

    # red pixel filtering & if wanted resulting image can be stored (outcommented)
    maskedhsv_denoised_red = maskhsvdenoise_red(img)
    im_red = maskedhsv_denoised_red
    print "segmented image red: ", fil
    #saveimagejpeg(image=im_red, name=outfolder+"/segmented/"+photoname+"_red")

    # merging of red & green pixel image & resulting image will be stored (..._merged)
    im_green=im_green +im_red
    print "merged files: ", fil
    saveimagejpeg(image=im_green, name=outfolder+"/segmented/"+photoname+"_merged")

else:
    # green image filtering for dates where no red leaves were present --> resulting image will be saved (..._green)
    maskedhsv_denoised_green = maskhsvdenoise_green(img)
    im_green = maskedhsv_denoised_green
    print "segmented image green: ", fil
    saveimagejpeg(image=im_green, name=outfolder+"/segmented/"+photoname+"_green")

# possibility to save grey-scale picture of whole tray
#im_grey=rgb2grey(im)
#saveimagejpeg(image=im_grey, name=outfolder + "/greyscale/" + photoname + "_grey")

## Query for pot index

print('cropping image...')
fileindex=outfolder+"\\"+"index_pots_pertray.tsv"

table=readtabtable(filename=fileindex)
# print table

# number and names of rows and columns in the picture --> according to the number of positions defined in "index_pots_pertray.txt"
rows= ["A", "B",  "C",  "D", "E", "F"]
columns=[1,2,3,4,5]

## Masking, grey-scaling and pixel counting

# csv file in which results for each tray will be saved separately
csvname=outfolder+"/results/"+timestring+"_"+photoname+"_results_pixel_count.csv"
print csvname

listoutcount=[]

# loop through all pot positions
for r in rows:
  for c in columns:
    for t in table:
     if "row" in t:
        continue
     if str(t[0]) == r and float (t[1]) ==float(c):
        # center point coordinates of circle (comes from "index_pots_pertray.txt" file; loops through all positions)
        x3= int(t[6])
        y3= int(t[7])

        # creates black mask with same size as image --> could be done separately for each filtered colour (outcommented; similar downwards in this loop)
        mask_green = np.zeros(im_green.shape, np.uint8)
        #mask_red = np.zeros(im_red.shape, np.uint8)

        # creates hole at specific pot position
        cv2.circle(mask_green, (x3, y3), 300, (255, 255, 255), -1)
        #cv2.circle(mask_red, (x3, y3), 300, (255, 255, 255), -1)

        # mask layer will be put over the pixel image & can be saved if wanted (outcommented)
        circle_green = cv2.bitwise_and(mask_green, im_green)
        #saveimagejpeg(image=circle_green, name=outfolder + "/greyscale/" + photoname + "_circle_green" + str(r) + str(c))
        #circle_red = cv2.bitwise_and(mask_red, im_red)
        #saveimagejpeg(image=circle_red, name=outfolder + "/greyscale/" + photoname + "_circle_red" + str(r) + str(c))

        # RGB image will be transformed into greyscale image & can be saved if wanted (outcommented)
        crop_grey_green = rgb2grey(circle_green)
        #crop_grey_red = rgb2grey(circle_red)
        #saveimagejpeg(image=crop_grey_green, name=outfolder + "/greyscale/" + photoname + "_grey_green" + str(r) + str(c))
        #saveimagejpeg(image=crop_grey_red, name=outfolder + "/greyscale/" + photoname + "_grey_red" + str(r) + str(c))

        # count green & red pixels
        count_green = cv2.countNonZero(crop_grey_green)
        #count_red = cv2.countNonZero(crop_grey_red)

        # produce the data line in the csv file: date image was taken, image name (includs date, tray number and treatment), tray position, number of counted pixels
        traypos=str(r)+str(c)
        towrite=[str(timestring),str(photoname),str(traypos),str(count_green)] #,str(count_red)
        listoutcount.append(towrite)

## Status of progress

if not listoutcount:
  print "Something went wrong, listoutcount is empty !!!"

outcount=open(csvname,"w")
for line in listoutcount:
    outcount.write(str(','.join(line)+"\n"))
outcount.close()

print "csv written"
print "Finished child process ..."
