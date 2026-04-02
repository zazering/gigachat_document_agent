import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

authorization = os.getenv("GIGACHAT_CREDENTIALS")

payload={
  'scope': 'GIGACHAT_API_PERS'
}

# to get Token to be able to communicate with API
# RqUID: you can generate it by yourself or get it in studio panel automatically
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'b1770a5b-f3d5-4f15-a91a-d82408c66795',
  'Authorization': f'Basic {authorization}'
}
# verify = False - to prevent ssl error
response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)