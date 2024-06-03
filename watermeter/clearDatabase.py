import sqlite3
import json
from datetime import datetime, timedelta

with open('config.json') as f:
	config = json.load(f)

databaseName = config['clearDatabase']['databaseName']
dayBack = config['clearDatabase']['dayBack']

daysAgo = datetime.now() - timedelta(days = dayBack)
daysAgo = daysAgo.isoformat()

connector = sqlite3.connect(databaseName)
cursor = connector.cursor()
cursor.execute("DELETE FROM photos WHERE photoTime < ?", (daysAgo,))
connector.commit()
connector.close()

print("Tabulka fotiek vycistena")
