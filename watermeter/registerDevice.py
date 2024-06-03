import requests
import json

flow_url = ''

with open('config.json') as j :
    config = json.load(j)

data = {
    'table': config['registerDevice']['table'],
    'DName': config['registerDevice']['DName'],
    'IDDevice': config['registerDevice']['IDDevice'],
    'Address': config['registerDevice']['Address'],
    'Email': config['registerDevice']['Email'],
}

response = requests.post(flow_url, json=data)

if response.status_code == 202:
    print("Dáta úspešne odoslané do Power Automate Flow.")
else:
    print(f"Chyba pri odosielaní dát: {response.status_code} - {response.text}")
