from fpdf import FPDF
import numpy as np
import argparse
import shutil
import pafy
import cv2
import os

parser = argparse.ArgumentParser("Convert YouTube videos to PDF!")
parser.add_argument("--url", required=True, dest='url', type=str,	help="YouTube-video URL")
parser.add_argument("--skip", required=True, dest='skip', type=int, help="Seconds to skip")
args = parser.parse_args()

video = pafy.new(args.url)
print(video.title)

best = video.getbest()
print(best.resolution, best.extension)

def dhash(image, hashSize=8):
    # convert the image to single-channel grayscale and resize the grayscale image,
    # adding a single column (width) so we can compute the horizontal gradient
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hashSize + 1, hashSize))
    #print(gray.shape,'\t',resized.shape,'\n',resized,'\n',type(resized))

    # compute the (relative) horizontal gradient between adjacent column pixels
    diff = resized[:, 1:] > resized[:, :-1]
    #print('\n',diff)

    # convert the difference image to a hash
    return sum([2 ** idx for (idx, value) in enumerate(diff.flatten()) if value])

cap = cv2.VideoCapture(best.url)
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

os.makedirs('./Output', exist_ok=True)

frame_id = 0
hashes, frame_ids = [], []

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame_id += 1 
        if frame_id < 24*args.skip: continue # Skipping first 10s (default) - assuming 24 fps

        frame_location = './Output/'+str(frame_id)+'.jpeg'
        h = dhash(frame)
        
        if h not in hashes:
            hashes.append(h)
            frame_ids.append(frame_id)

            #if frame_id-1 not in frame_ids:
            if set([frame_id-1, frame_id-2, frame_id-3, frame_id-4]).isdisjoint(frame_ids):
                cv2.imwrite(frame_location, frame)
                print(f"frame {str(frame_id)} with hash {h} saved.")
    else:
        break  

cap.release()
print("Video processed! Converting to PDF ...")
print(os.listdir('./Output'))

pdf = FPDF(orientation = 'Landscape', unit = 'mm', format='A4')

WIDTH = 210
HEIGHT = 297

def sortfiles(imagefiles):
    sorted_list1 = []
    for image in imagefiles:
        sorted_list1.append(int(image.split('.')[0]))
    sorted_list1.sort()
    
    sorted_list2 = []
    for element in sorted_list1:
        sorted_list2.append(str(element)+'.jpeg')
    return sorted_list2

for image in sortfiles(os.listdir('./Output')):
    pdf.add_page()
    pdf.image('./Output/'+str(image), x=10, y=10, w = HEIGHT-10)

shutil.rmtree('./Output')
pdf.output(str(video.title)+'.pdf')

print("Conversion successful! " + str(video.title)+'.pdf'+ " ---> Stored at "+str(os.getcwd()))
