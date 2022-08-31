#!/bin/bash

for x in $(cat urls.txt)
do
    python /home/runner/work/YouTube-video-to-PDF-PPT-Images/YouTube-video-to-PDF-PPT-Images/YouTube-video-to-PDF-PPT-Images/main.py --skip 10 --silent_del true --file images --url $x
done
