import requests as rq
import os

authorization = {
    "apiKey": os.getenv("ENCRYPTION_KEY")
}