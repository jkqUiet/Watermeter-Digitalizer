import sys
from PIL import Image
import json

with open('config.json') as f:
    config = json.load(f)

imgPath = config['cropper2']['imgPath']
gearCount = config['cropper2']['gearCount']
gearSize = config['cropper2']['gearSize']
gearSpace = config['cropper2']['gearSpace']
outputPath = config['cropper2']['outputPath']
def split(numberCount, wheelWidth, spaceWidth):
    try:
        img = Image.open(imgPath)
        width, height = img.size
        for i in range(numberCount - 1):
            print(img.size)
            imgX = outputPath+str(i)+".jpg"
            left = i * wheelWidth + spaceWidth * i
            right = min((i + 1) * wheelWidth + spaceWidth * i, width)
            number = img.crop((left, 0, right, height))
            number.save(imgX)
        imgX = outputPath + str(numberCount-1) + ".jpg"
        number = img.crop(((numberCount -1) * wheelWidth + spaceWidth * (numberCount-1), 0, width, height))
        number.save(imgX)
        img.close()
    except Exception as e:
        print("Problem v cropperiOnce: ", e)

if __name__ == "__main__":
    split(gearCount, gearSize, gearSpace)
