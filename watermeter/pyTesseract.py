import pytesseract
from PIL import Image
import sqlite3
from datetime import datetime
import json
import subprocess

with open('config.json') as f:
    config = json.load(f)

tesseractTable = config['pyTesseract']['tesseractTable']
dataAzureTable = config['pyTesseract']['dataAzureTable']
maxLiterCount = config['pyTesseract']['maxLiterCount']
databaseName = config['pyTesseract']['databaseName']
imagePath = config['pyTesseract']['imagePath']
gearImagePath = config['pyTesseract']['gear']
pathToGearCropper = config['pyTesseract']['gearCropper']
gearCount = config['cropper2']['gearCount']

def extractNumbersImage(image_path):
    try:
        with Image.open(image_path) as img:
            c_config = r'--oem 3 --psm 6'            
            result = pytesseract.image_to_string(img, config = c_config)
            numbers = ''.join(filter(str.isdigit, result))
            return numbers
    except FileNotFoundError:
        print("Subor nenajdeny")

def extractNumberGear(image):
    c_config = r'--oem 3 --psm 10'            
    result = pytesseract.image_to_string(image, config = c_config)
    number = ''.join(filter(str.isdigit, result))
    return number

def databaseSave(numbers, timestamp, validation):
    try:
        connector = sqlite3.connect(databaseName)
        cursor = connector.cursor()
        cursor.execute("SELECT MAX(id) FROM photos")
        photoId = cursor.fetchone()[0]
        if photoId == "":
            print("Vo fotkach sa nenachadza nic!!!")
            return
        photoId = int(photoId)
        numbersInteger = int(numbers)
        print("Extracted Numbers String", numbers)
        print("Extracted Numbers Int", str(numbersInteger))
        cursor.execute("INSERT INTO " + tesseractTable + \
                        " (extractionTime, photoId, dataValue, dataText, validationSign) \
                       VALUES (?,?,?,?,?)", (timestamp, photoId, numbersInteger, numbers, validation))
        connector.commit()
        connector.close()
    except sqlite3.Error as e:
        print("PyTesseract::databaseSave, problem s DB", e)
    
def validate(numbers):
    dataValue = -1
    try:
        connector = sqlite3.connect(databaseName)
        cursor = connector.cursor()
        cursor.execute("SELECT COUNT(*) FROM " + tesseractTable)
        count = cursor.fetchone()[0]
        if (int(count) == 0):
            return 1, -1
        cursor.execute("SELECT dataValue FROM " + tesseractTable\
                        + " WHERE "+ tesseractTable +".id = (SELECT MAX("\
                        + dataAzureTable +".id) FROM " \
                        + tesseractTable + " JOIN dataAzure on ("\
                        + tesseractTable +".id = " + dataAzureTable \
                        +".tesseractID))")
        row = cursor.fetchone()
        dataValue = row[0] if row else None
        cursor.close()
        if dataValue is None:
            return 0, -1
        numbersInteger = int(numbers)
        if (abs(numbersInteger - dataValue) < maxLiterCount):
            return 1, -1
        else:
            return 0, dataValue
    except sqlite3.Error as e:
        print("PyTesseract::validate, problem s DB")

def secondValidation(dataValue):
    strDataValue = str(dataValue)
    finalData = ""
    for i in reversed(range(gearCount)):
        with Image.open(gearImagePath + str(i) + ".jpg") as img:
            gearValue = extractNumberGear(img)
            print(gearValue)
            if dataValue == -1:
                finalData = gearValue + finalData
            elif gearValue:
                if (int(gearValue) > int(strDataValue[i])):
                    finalData = gearValue + finalData
                else:
                    finalData = strDataValue[i] + finalData
            else:
                finalData = strDataValue[i] + finalData
    return finalData

if __name__ == "__main__":
    numbers = extractNumbersImage(imagePath)
    timestamp = datetime.now().isoformat()
    print(numbers)
    validation, previousValue = validate(numbers) 
    if (validation == 0):
        subprocess.call(['python', pathToGearCropper])
        numbers = secondValidation(previousValue)
        validation = 1
    databaseSave(numbers, timestamp, validation)
