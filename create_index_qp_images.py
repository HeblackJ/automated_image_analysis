## Produces files for images to analyze with respective index ##

import sys, os, time

from subprocess import *

# inquire working folder (same folder as the date specific images)
try:
    infolder=sys.argv[1]
except IndexError:
    infolder=os.getcwd()

# reading of list of images to be analyzed
command="cd "+infolder+" & dir /b *.JPG > images_to_analyze.txt"
call(command,shell=True)

images_to_analyze=open(infolder+"\\"+"images_to_analyze.txt","r")
filesimage=[x.replace("\n","") for x in images_to_analyze]

# indexing of images to be analyzed
counterimage=1

index_images=[]
print('generating the index of images and dates')
for fil in filesimage:
	(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(infolder+"\\"+fil)
	mytime=time.ctime(mtime)
	mytime=mytime.replace("  "," ").split(" ")

	timestring="2020"+"-"+mytime[1]+"-"+mytime[2] # year has to be updated manually
 
	row=[ str(fil),str(timestring),str(counterimage)]
	index_images.append(row)
	print row

	counterimage=counterimage+1

	if counterimage == 50:
		counterimage=1
	else:
		pass

# produces file that lists image to be analyzed with date of image and index number
output=open(infolder+"\\"+"index_images.txt","w")
for line in index_images:
	output.write(str(','.join(line)+"\n"))

output.close()

print "csv written"

