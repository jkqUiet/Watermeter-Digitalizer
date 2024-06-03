#!/bin/bash

BASEFOLDER="/home/bobo/Documents/watermeter"

cd "$BASEFOLDER" || exit 1

python azCandidateRecognize.py
python pushDataAzure.py
