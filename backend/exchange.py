import requests as rq
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://demo.trading212.com/api/v0/equity/account/summary"

apiId = os.getenv("TR212_API_ID")
apiKey = os.getenv("TR212_API_KEY")

response = rq.get(url,auth=(apiId, apiKey))

if response.status_code == 200:
    data=response.json()
    print(data)
else:
    print(f"Err {response.status_code}")