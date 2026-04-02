import os
import time
import uuid
from datetime import datetime
import requests
import urllib3
from dotenv import load_dotenv, set_key

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GigaChatTokenManager:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("TOKEN_URL")
        self.credentials = os.getenv("GIGACHAT_CREDENTIALS")
        self.access_token = None
        self.expires_at = 0
        self.load_saved_token()

    def load_saved_token(self):
        self.access_token = os.getenv("TOKEN_ACCESS_API")
        expires_str = os.getenv("TOKEN_EXPIRES_AT")
        if expires_str:
            self.expires_at = int(expires_str)

    def is_token_valid(self):
        # 5 min gap
        return self.access_token and time.time() * 1000 < self.expires_at - 300000

    def get_new_token(self):
        rquid = uuid.uuid4()
        payload = {'scope' : "GIGACHAT_API_PERS"}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(rquid),
            'Authorization': f'Basic {self.credentials}'
        }

        response = requests.post(self.url, headers=headers, data=payload, verify=False)
        data = response.json()
        self.access_token = data['access_token']
        self.expires_at = data['expires_at']

        set_key('.env', 'TOKEN_ACCESS_API', self.access_token)
        set_key('.env', 'TOKEN_EXPIRES_AT', str(self.expires_at))

        print(f"New token expires: {datetime.fromtimestamp(self.expires_at / 1000)}")
        return self.access_token

    def get_token(self):
        if not self.is_token_valid():
            print("Token expired")
            return self.get_new_token()
        else:
            print("Token valid")
            return self.access_token



# Usage
if __name__ == "__main__":
    manager = GigaChatTokenManager()
    token = manager.get_token()
    print(f"Current token: {token[:20]}...")