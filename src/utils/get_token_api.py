import requests
import uuid
import os
from dotenv import load_dotenv

# !Deprecated code, please use GigaChatTokenManager!

load_dotenv()

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

RqUID = uuid.uuid4()

authorization = os.getenv("GIGACHAT_CREDENTIALS")

payload={
'scope': 'GIGACHAT_API_PERS'
}

# Expires every 30 min
# to get Token to be able to communicate with API
# RqUID: you can generate it by yourself or get it in studio panel automatically
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': f'{RqUID}',
  'Authorization': f'Basic {authorization}'
}
# verify = False - to prevent ssl error / or you need to download ssl certificates
response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)