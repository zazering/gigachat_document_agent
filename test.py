#test gigachat.py   
from langchain_gigachat import GigaChat
from dotenv import load_dotenv
import os

llm = GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    model="GigaChat-2-Lite",
    verify_ssl_certs=False,
    temperature=0.1
)

response = llm.invoke("Привет! Как дела?")
print(response.content)


