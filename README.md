# YouTube-video-to-PDF-PPT-Images
Convert YouTube videos to PDF, PPT, or Images! <br>
Takes in a URL of a YouTube video and outputs a PDF/PPT/Images comprising of all the unique frames. 

### Create a conda environment
```
$ conda create --name url_convert python=3.7
$ conda activate url_convert
```
### Install the required dependencies
```
$ cd YouTube-video-to-PDF-PPT-Images
$ pip install -r requirements.txt
```
### Demo
```
$ python main.py --skip 10 --file pdf --url https://www.youtube.com/watch?v=Gv9_4yMHFhI&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF

Conversion successful! A Gentle Introduction to Machine Learning.pdf ---> Stored at /home/ubuntu/YouTube-video-to-PDF-PPT-Images/Output/
```

#### Procedure:
- Create a numerical representation of each frame (this numerical representation is called hash)
- When two images have the same hash, they are considered duplicates

1. Convert the image to a single-channel grayscale image.
2. Resize the image according to the hashSize (the algorithm requires that the width of the image have exactly 1 more column than the height)
3. Compute the relative horizontal gradient between adjacent column pixels. This is now known as the “difference image.”

Refer [pyimagesearch](https://pyimagesearch.com/2020/04/20/detect-and-remove-duplicate-images-from-a-dataset-for-deep-learning/)

#### Flags
```
"--url", YouTube-video URL (required)
"--file", Required file type: 'pdf', 'ppt', 'images' (required)
"--skip", Starting seconds to skip 
(defaut: 0)
"--path", Download location
(default: ./Output/)
"--download", Downloads video only
(default: False)
```
