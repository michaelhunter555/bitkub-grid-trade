import os
import json
import httpx
import time
from utils.gen_sign import gen_sign
from dotenv import load_dotenv

load_dotenv()

BITKUB_API_KEY = os.environ.get('BITKUB_API_KEY')
BITKUB_SECRET_KEY = os.environ.get('BITKUB_API_SECRET')

async def place_bid(symbol="thb_sol", amount=1, rate=1):
    #Set up Bitkub host, path and api keys
    host = 'https://api.bitkub.com'
    path = '/api/v3/market/place-bid'
    api_key = BITKUB_API_KEY
    api_secret = BITKUB_SECRET_KEY

    #Timestamp
    ts = str(round(time.time() * 1000))
    
    #Test SOL for now, pass parameters amount and rate
    reqBody = {
        'sym': symbol, # crypto you want to buy
        'amt': amount, #how much you want too buy
        'rat': rate, #price you want to buy at
        'typ': 'limit'
    }

    #payload to pass with our signature
    payload = [ts, 'POST', path, json.dumps(reqBody)]

    #Create signature
    sig = gen_sign(api_secret, ''.join(payload))

    #Prepare headers
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-BTK-TIMESTAMP': ts,
        'X-BTK-SIGN': sig,
        'X-BTK-APIKEY': api_key
    }

    #Create async request
    async with httpx.AsyncClient() as client:
        response = await client.post(host + path, headers=headers, json=reqBody)
        print(response.text)
        return response
