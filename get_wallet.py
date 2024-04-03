import os
import json
import httpx
import time
from utils.gen_sign import gen_sign
from dotenv import load_dotenv

load_dotenv()

BITKUB_API_KEY = os.environ.get('BITKUB_API_KEY')
BITKUB_SECRET_KEY = os.environ.get('BITKUB_API_SECRET')

async def get_user_wallet():
    host = "https://api.bitkub.com"
    path = "/api/v3/market/wallet"
    api_key = BITKUB_API_KEY
    api_secret = BITKUB_SECRET_KEY

    ts = str(round(time.time() * 1000))

   payload = [ts, 'POST', path, '']

   sig = gen_sign(api_secret, ''.join(payload))

     headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-BTK-TIMESTAMP': ts,
        'X-BTK-SIGN': sig,
        'X-BTK-APIKEY': api_key
    }

    #Create async request
    async with httpx.AsyncClient() as client:
        response = await client.post(host + path, headers=headers)
        print(response.text)
        return response