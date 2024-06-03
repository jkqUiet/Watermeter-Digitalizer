
import sqlite3
from datetime import datetime, timedelta
import json

with open('config.json') as f:
    config = json.load(f)

tesseractTable = config['pyTesseract']['tesseractTable']
databaseName = config['pyTesseract']['databaseName']

def databaseSave(numbers):
    try:
        connector = sqlite3.connect(databaseName)
        cursor = connector.cursor()
        print("Zapisujem inicializacne hodnoty", numbers)
        cursor.execute("INSERT INTO " + tesseractTable + " (extractionTime, photoId, dataValue, dataText, validationSign) \
                       VALUES (?,?,?,?,?)", (timestamp, -1, int(numbers), numbers, -1))
        connector.commit()
        connector.close()
    except sqlite3.Error as e:
        print("INIT::databaseSave, problem s DB", e)

if __name__ == "__main__":
    value = 0
    while True:
        value = input("Zadajte aktualnu hodnotu vodomera : ")
        if value.isdigit():
            break

    timestamp = datetime.now() - timedelta(days = -3)
    databaseSave(int(value))
