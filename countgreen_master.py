## Main program with workflow & system times ##

import datetime
import os
import sys
import time
from subprocess import *

now1=time.strftime("%d-%b-%Y %H:%M:%S")
print ("time start process: ", now1)

## Folder in which to work

try:
    infolder=sys.argv[1]
except IndexError:
    infolder=os.getcwd()

try:
    outfolder=sys.argv[2]
except IndexError:
    outfolder=infolder

## Create output folders --> if you want to save greyscale or sub-step pictures you need to uncomment "greyscale" folder creation

call("mkdir segmented",shell=True,cwd=outfolder)
call("mkdir results",shell=True,cwd=outfolder)
#call("mkdir greyscale",shell=True,cwd=outfolder)

## Index how many images you have to analyse & generate number --> produces .txt file

print("create index images")
command="python create_index_qp_images.py " + infolder
call(command,shell=True)

index=open(infolder+"\\"+"index_images.txt","r")
index=[x.replace("\n","").split(",") for x in index]
keys=[x[0].split("/")[-1].split(".")[0] for x in index]
values=[x[2] for x in index]

indexdic={}
for k, v in zip(keys,values):
    indexdic[k]=v

if not indexdic:
    print ("Something went wrong, no correct index !!!")
else:
    print ("index of images and qp numbers generated")
print(indexdic)

## Image analysis workflow

print("find images to analyse")

# read list of images:to_analyze
images_to_analyze=open(infolder+"\\"+"images_to_analyze.txt","r")
filesimage=[x.replace("\n","") for x in images_to_analyze]

# read each image --> based on qp number
import time

counterlist=0
counter=0
maxparallel=20

for fil in filesimage:
    counterlist=counterlist+1
    print ("->working over this file",fil)

# prints what file is currently worked on
    photoname=fil.split(".")[0].split("/")[-1]
    qpnum=indexdic[photoname]

# forwarding to actual image analysis (colour filtering, merging, masking, grey-scaling, pixel counting)
    cmd="python countgreen_child.py"+" "+qpnum + " " + fil + " " +outfolder
    p = Popen(cmd, shell=True, stdout=PIPE,stderr=PIPE)

# check for errors. problem is that you have to wait until it finishes .. so no parallel
    out, err = p.communicate()  
    if err:
        print ("standard error of subprocess:")
        print (err)

# set a limit to the parallelisation
    counter=counter+1
    print (counter)
    
    if counter == maxparallel:
        p.wait()
        counter=0
    else:
        pass

# wait in the last file iteration.
    if counterlist == len(filesimage):
        p.wait()
    else:
        pass
# out of loop

## Merge all spreadsheets and produce a combined one ("...bigcsv..."; for each picture folder separately)

command="dir /b *.csv > spreadsheets_to_analyze.txt"
call(command,shell=True, cwd=outfolder+'\\'+'results')
spreadsheets=open(outfolder+"\\results\\"+"spreadsheets_to_analyze.txt","r")
spreadsheets=[x.replace("\n","") for x in spreadsheets]

# read each file and append to the big csv
bigcsv=["date,image,position,green\n"]

for csv in spreadsheets:
    csvread=open(outfolder+"\\results\\"+csv,"r")
    csvread=[x for x in csvread]
    for row in csvread:
        bigcsv.append(row)

csvname=outfolder+"\\results\\"+"bigcsv_results_pixel_count.csv"
outbigcsv=open(csvname,"w")
for line in bigcsv:
    outbigcsv.write(line)
outbigcsv.close()

## Output end time & duration of analysis

now2=time.strftime("%d-%b-%Y %H:%M:%S")

print ("Finished master process at time ", now2)

d1 = datetime.datetime.strptime(now1, '%d-%b-%Y %H:%M:%S')
d2 = datetime.datetime.strptime(now2, '%d-%b-%Y %H:%M:%S')

difftime = (d2 - d1).total_seconds() / 60
print ("Total time of the analysis: ", difftime, " minutes")
