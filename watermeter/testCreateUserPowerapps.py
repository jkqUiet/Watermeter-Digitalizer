import requests
import json

flow_url = ''

data = {
    'table': 'Contact',
    'FName': 'Ferko',
    'LName': 'Hrasek',
    'Email': 'jozef.kompan@student.tuke.sk',
    'PNumber': '012345',
}

response = requests.post(flow_url, json=data)

if response.status_code == 202:
    print("Dáta úspešne odoslané do Power Automate Flow.")
else:
    print(f"Chyba pri odosielaní dát: {response.status_code} - {response.text}")
