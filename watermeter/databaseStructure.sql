CREATE TABLE photos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  photo BLOB NOT NULL,
  photoTime TIMESTAMP
);

CREATE TABLE tesseractDataExtracted (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  extractionTime TIMESTAMP NOT NULL,
  photoId INTEGER,
  dataValue INTEGER NOT NULL,
  dataText TEXT,
  validationSign INTEGER,
  FOREIGN KEY (photoId) REFERENCES photos(id)
);

CREATE TABLE dataAzure (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dataText TEXT,
  dataValue INTEGER,
  extractionTime TIMESTAMP NOT NULL,
  photoId INTEGER,
  tesseractID INTEGER, 
  FOREIGN KEY (photoId) REFERENCES photos (id),
  FOREIGN KEY (tesseractID) REFERENCES tesseractDataExtracted(id)
);
