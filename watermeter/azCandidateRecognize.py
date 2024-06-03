from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.exceptions import ResourceNotFoundError

import pytesseract
from PIL import Image
import sqlite3
from datetime import datetime, timedelta
import socket
import subprocess
import json

with open('config.json') as f:
    config = json.load(f)

tesseractTable = config['azCandidateRecognize']['tesseractTable']
dataAzureTable = config['azCandidateRecognize']['dataAzureTable']
photoTable = config['azCandidateRecognize']['photoTable']
maxLiterCount = config['azCandidateRecognize']['maxLiterCount']
timePeriod = config['azCandidateRecognize']['timePeriod']
tmpImage = config['azCandidateRecognize']['tmpImage']
imagePath = config['azCandidateRecognize']['imagePath']
gearCount = config['cropper2']['gearCount']

endpoint = ""
key = ""
databaseName = config['azCandidateRecognize']['databaseName']

cropper = config['azCandidateRecognize']['cropper']

def checkConnection():
    try:
        socket.create_connection(("8.8.8.8"), timeout=2)
        return True
    except OSError:
        print("No internet connection available")
        return False

def chooseCandidate(validationSign): # toto sa da upravit aj na doposielanie neposlanych dat tym ze upravim timeperiod ak nenajde kandidata berie prve vhodne
    connector = sqlite3.connect(databaseName)
    cursor = connector.cursor()
    halfHour = (datetime.now() - timedelta(minutes = timePeriod)).isoformat() # za poslednu polhodinu
    cursor.execute("SELECT "+ tesseractTable + ".id, " + photoTable + ".id, "+ photoTable +".photo," + tesseractTable + ".dataText," \
                    + tesseractTable + ".dataValue FROM " + photoTable +
                    " JOIN " + tesseractTable +
                    " ON (" + tesseractTable + ".photoId = " + photoTable + ".id)" +
                    " LEFT JOIN " + dataAzureTable +
                    " ON (" + tesseractTable + ".id = " + dataAzureTable + ".tesseractID)" +
                    " WHERE " + dataAzureTable + ".id IS NULL AND " + tesseractTable + ".extractionTime >= ?" +
                    " AND " + tesseractTable + ".validationSign = ?" +
                    " ORDER BY " + tesseractTable + ".extractionTime DESC" +
                    " LIMIT 1", (halfHour, validationSign,))
    result = cursor.fetchone() # tu je vybrana fotka kandidata
    if result:
        id, photoId, cPhoto, tesDataS, tesDataI = result
        return id, photoId, cPhoto, tesDataS, tesDataI
    else:
        return None
    
#vytvori preprocessnuty file pre azure, s tym ze ho vytiahne z databazy, je to uz dobry kandidat. 
def preprocessFile(photo):
    try:
        with open(tmpImage, "wb") as f:
            f.write(photo)
        args = [imagePath, tmpImage]
        subprocess.run(["python", cropper] + args)
        command = ["convert", tmpImage, "-resize", "800x", "-density", "600", "-unsharp", "0x1+1+0", tmpImage]
        subprocess.run(command, check=True)
        print("Preprocessing prebehol.")
    except subprocess.CalledProcessError as e:
        print("Problem s preprocessingom", e)

def databaseSave(numbers, extractionTime, photoId, tesseractId):
    numbersInteger = int(numbers)
    try:
        connector = sqlite3.connect(databaseName)
        cursor = connector.cursor()
        cursor.execute("INSERT INTO " + dataAzureTable + " (dataText, dataValue, extractionTime, photoId, tesseractID) values (?,?,?,?,?)",\
                       (numbers, numbersInteger, extractionTime, photoId, tesseractId))
        connector.commit()
        connector.close()
    except sqlite3.Error as e:
        print("azureCandidateRecognize::databaseSave, problem s DB", e)

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

def analyze_read_from_image(photoPath):
    try:
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        with open(photoPath, "rb") as image_fd:
            poller = document_analysis_client.begin_analyze_document(
                "prebuilt-read", image_fd
            )
        result = poller.result()
        fValue = ""
        print("Document contains content: ", result.content)
        for page in result.pages:
            for line in page.lines:
                for character in line.content:
                    if isinstance(character, int) or (isinstance(character, str) and character.isdigit()):
                        fValue+=(str(character))
        return fValue
    except ResourceNotFoundError:
        print("Chyba obrazok v databaze, pripadne nenaslo kandidata")

if __name__ == "__main__":
    candidate = chooseCandidate(1)
    candidateFound = True
    if candidate:
        tesseractId, photoId, cPhoto, tesDataS, tesDataI  = candidate
    else:
        candidateFound = False
        candidate = chooseCandidate(0)
        tesseractId, photoId, cPhoto, tesDataS, tesDataI  = candidate
    preprocessFile(cPhoto)
    resultAzure = analyze_read_from_image(tmpImage)
    if (candidateFound):
        if ((len(resultAzure) == 0 and int(resultAzure) < tesDataI) and len(resultAzure) == gearCount):
            databaseSave(resultAzure, datetime.now().isoformat(), photoId, tesseractId)
        else:
            databaseSave(tesDataS, datetime.now().isoformat(), photoId, tesseractId)
    else:
        databaseSave(resultAzure, datetime.now().isoformat(), photoId, tesseractId)
    subprocess.run(["rm", tmpImage], check=False) # vymaze temp subor
