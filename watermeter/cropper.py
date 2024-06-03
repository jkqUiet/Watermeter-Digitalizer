import sys
from PIL import Image
import json

with open('config.json') as f:
    config = json.load(f)

leftEdge = config['cropper']['leftEdgePercentage']
topEdge = config['cropper']['topEdgePercentage']
rightEdge = config['cropper']['rightEdgePercentage']
bottomEdge = config['cropper']['bottomEdgePercentage']
rotation = config['cropper']['rotation']

def preprocessImage(inputFile, outputFile):
    try:
        img = Image.open(inputFile)
        width, height = img.size
        img = img.rotate(rotation)
        left_edge = width * leftEdge
        top_edge = height * topEdge
        right_edge = width * rightEdge
        bottom_edge = height * bottomEdge
        area = (left_edge, top_edge, right_edge, bottom_edge)
        cropped_img = img.crop(area)
        cropped_img.save(outputFile)
        img.close()
    except Exception as e:
        print("Problem v cropperi : ", e)

if __name__ == "__main__":
    inputFilename = sys.argv[1]
    outputFilename = sys.argv[2]

    preprocessImage(inputFilename, outputFilename)
