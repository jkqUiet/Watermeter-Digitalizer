#!/bin/bash

BASEFOLDER="/home/bobo/Documents/watermeter"

cd "$BASEFOLDER" || exit 1

python ledOn.py
raspistill -q 100 -o image.jpg
python ledOff.py
python databaseSaveImage.py image.jpg
python cropper.py image.jpg cropped.jpg
./resizeSharpen.sh
python pyTesseract.py

