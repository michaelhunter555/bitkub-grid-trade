import os
import json
import httpx
import time
from util.gen_sign import gen_sign
from dotenv import load_dotenv

load_dotenv()

BITKUB_API_KEY = os.environ.get('BITKUB_API_KEY')
BITKUB_SECRET_KEY = os.environ.get('BITKUB_API_SECRET')


async def get_ticker(sym="thb_sol"):
    host = 'https://api.bitkub.com'
    path = '/api/market/ticker'
    api_key = BITKUB_API_KEY
    api_secret = BITKUB_SECRET_KEY

    ts = str(round(time.time() * 1000))

    reqQuery = {
        'sym': sym #ticker symbol
    }

    payload = [ts, 'GET', path, '']
    sig = gen_sign(api_secret, ''.join(payload))

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-BTK-TIMESTAMP': ts,
        'X-BTK-SIGN': sig,
        'X-BTK-APIKEY': api_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(host + path, headers=headers, params=reqQuery)
        data = response.json()

        percent_change = data['THB_SOL']['percentChange']
        print(data)
        return data