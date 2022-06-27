# YouTube-video-to-PDF
Takes in a URL of a YouTube video and outputs a PDF comprising of all the unique frames. 

### Create a conda environment
```
$ conda create --name video2pdf python=3.7
$ conda activate video2pdf
```
### Install the required dependencies
```
$ cd YouTube-video-to-PDF
$ pip install -r requirements.txt
```
### Demo of video2pdf
```
$ python video.py --skip 10 --url https://www.youtube.com/watch?v=LcYmoLSs4Tc&feature=youtu.be
Conversion successful! StatQuest Trailer, 2019.pdf ---> Stored at /home/ubuntu/youtube-video2pdf
```

#### Procedure:
- Create a numerical representation of each frame (this numerical representation is called hash)
- When two images have the same hash, they are considered duplicates

1. Convert the image to a single-channel grayscale image.
2. Resize the image according to the hashSize (the algorithm requires that the width of the image have exactly 1 more column than the height)
3. Compute the relative horizontal gradient between adjacent column pixels. This is now known as the “difference image.”


Refer [pyimagesearch](https://pyimagesearch.com/2020/04/20/detect-and-remove-duplicate-images-from-a-dataset-for-deep-learning/)
