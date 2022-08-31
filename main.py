from convert import images2pdf, images2ppt
import argparse
import shutil
import pafy
import cv2
import os

parser = argparse.ArgumentParser("Convert YouTube videos to PDF, PPT and Images!")
parser.add_argument("--url", required=True, dest='url', type=str, help="YouTube-video URL")
parser.add_argument("--skip", required=False, default=0, dest='skip', type=int, help="Starting seconds to skip")
parser.add_argument("--path", required=False, default=os.getcwd()+'/Output/', help="Download location")
parser.add_argument("--file", required=True, dest='file', type=str, help="Required file type: pdf, ppt, images")
parser.add_argument("--download", required=False, dest='download', default=False, type=bool, help="downloads video only")
args = parser.parse_args()

print("Saving at ", args.path+video.title)

video = pafy.new(args.url)
print("Video Title:", video.title)

best = video.getbest()
print("Video Resolution:", best.resolution, "\nExtension:", best.extension)

if args.download:
    print(f"Downloading ---> {video.title}")
    best.download(quiet=False)

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

os.makedirs(args.path+video.title, exist_ok=True)

frame_id = 0
hashes, frame_ids = [], []

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame_id += 1 
        if frame_id < 24*args.skip: continue # Skipping first 10s (default) - assuming 24 fps

        frame_location = args.path+video.title+str(frame_id)+'.jpeg'
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

if args.file == 'pdf':
    images2pdf(name=video.title, location=args.path+video.title)
    shutil.rmtree(args.path+video.title)
elif args.file == 'ppt':
    images2ppt(name=video.title, location=args.path+video.title)
    shutil.rmtree(args.path+video.title)
elif args.file == 'images':
    print(f"Unique frames downloaded at {args.path+video.title}")
