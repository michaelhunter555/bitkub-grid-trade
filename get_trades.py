import os 
import time
import json
import httpx
from utils.gen_sign import gen_sign

from dotenv import load_dotenv

load_dotenv()

BITKUB_API_KEY = os.environ.get('BITKUB_API_KEY')
BITKUB_SECRET_KEY = os.environ.get('BITKUB_API_SECRET')

async def get_trades(symbol="thb_sol", limit=10):
    host = 'https://api.bitkub.com'
    path = '/api/market/trades'
    api_key = BITKUB_API_KEY
    api_secret = BITKUB_SECRET_KEY

    reqQuery = {
        'sym': symbol, #trades for said coin
        'lmt': limit, #amount of trades
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
        response = await client.post(host + path, headers=headers, params=reqQuery)
        print(response.text)
        return response