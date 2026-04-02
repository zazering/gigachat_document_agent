import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://gigachat.devices.sberbank.ru/api/v1/models"

TOKEN = os.getenv("TOKEN_ACCESS_API")
payload = {}
headers = {
    'Accept': 'application/json',
    "Authorization" : f"Bearer {TOKEN}"
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

models_data = response.json()
print("Data type: ", type(models_data))
with open('../models/gigachat_models.json', 'w', encoding='utf-8') as f:
    json.dump(models_data, f, ensure_ascii=False, indent=2)

print("save in json file gigachat_models.json")
for model in models_data['data']:
    if model['type'] == 'chat':
        print(f"- {model['id']}")
