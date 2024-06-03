import requests
import sqlite3
import base64
from PIL import Image
import io
import json

with open('config.json') as f:
    config = json.load(f)

flow_url = ''
dataAzureTable = config['pushDataAzure']['dataAzureTable']
databaseName = config['pushDataAzure']['databaseName']
table = config['pushDataAzure']['table']
iddevice = config['pushDataAzure']['IDDevice']

def getDataDatabase():
    connector = sqlite3.connect(databaseName)
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM " + dataAzureTable + " ORDER BY extractionTime DESC")
    result = cursor.fetchone()
    return result

def getPhoto(photoId):
    connector = sqlite3.connect(databaseName)
    cursor = connector.cursor()
    cursor.execute("SELECT photo FROM photos WHERE id = ?", (photoId,))
    result = cursor.fetchone()[0]
    return result

def resizePhoto(photo):
    with Image.open(io.BytesIO(photo)) as img:
        img = img.resize((300, 180), Image.ANTIALIAS)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        newPhoto = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    return newPhoto

def createData(row, photo):
    data = {
        'table': table,
        'ExtractionTime': row[3],
        'IDDevice': iddevice,
        'IDPhoto': int(row[4]),
        'IDTesseract' : int(row[5]),
        #'Photo' : photo 
        'DNumber' : int(row[2]),
        'DText' : row[1]
    }
    return data

if __name__ == "__main__":
    row = getDataDatabase()
    photo = getPhoto(int(row[4]))
    photo = resizePhoto(photo)
    data = createData(row, photo)
    response = requests.post(flow_url, json=data)
    if response.status_code == 202:
        print("Dáta úspešne odoslané do Power Automate Flow.")
    else:
        print(f"Chyba pri odosielaní dát: {response.status_code} - {response.text}")
