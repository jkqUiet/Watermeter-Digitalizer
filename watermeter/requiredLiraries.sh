#!/bin/bash

sudo apt update
sudo apt install -y tesseract-ocr
sudo apt install -y python3 python3-pip
sudo apt-get install imagemagick
pip3 install azure-core azure-ai-formrecognizer
pip3 install pillow
sudo apt install -y sqlite3
pip3 install RPi.GPIO

