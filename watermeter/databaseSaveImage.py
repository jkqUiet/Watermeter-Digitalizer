
import sqlite3
import sys
from datetime import datetime
import json

with open('config.json') as f:
    config = json.load(f)

databaseName = config['databaseSaveImage']['databaseName']

def save_photo_to_db(photo_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(databaseName)
        cursor = conn.cursor()

        # Read the photo file
        with open(photo_path, 'rb') as photo_file:
            photo_blob = photo_file.read()

        # Get the current timestamp
        current_time = datetime.now()

        # Insert the photo and timestamp into the 'photos' table
        cursor.execute("INSERT INTO photos (photo, photoTime) VALUES (?, ?)", (sqlite3.Binary(photo_blob), current_time))
        conn.commit()

        print("Fotka ulozena, cas ulozenia : ", current_time)

    except sqlite3.Error as e:
        print("Problem s databazou : ", e)

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python save_photo_to_db.py <photo_path>")
        sys.exit(1)

    photo_path = sys.argv[1]
    save_photo_to_db(photo_path)
