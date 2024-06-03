#!/bin/bash

convert cropped.jpg -resize 800x -density 600 -unsharp 0x1+1+0 cropped.jpg
convert cropped.jpg  -threshold 23% cropped_pyTesseract.jpg
