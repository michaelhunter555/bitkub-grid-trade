import os
import json
import httpx
import time
from utils.gen_sign import gen_sign
from dotenv import load_dotenv

load_dotenv()

BITKUB_API_KEY = os.environ.get('BITKUB_API_KEY')
BITKUB_SECRET_KEY = os.environ.get('BITKUB_API_SECRET')

async def cancel_order(symbol="thb_sol", order_id, sd, hash_string=""):
    host = 'https://api.bitkub.com'
    path = '/api/v3/market/cancel-order'
    api_key = BITKUB_API_KEY
    api_secret = BITKUB_SECRET_KEY

    ts = str(round(time.time() * 1000))
    reqBody = {
        'sym': symbol,
        'id': order_id,
        'sd': sd,
        'hash': hash_string,
    }

    payload = [ts, 'POST', path, json.dumps(reqBody)]

    sig = gen_sign(api_secret, ''.join(payload))
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-BTK-TIMESTAMP': ts,
        'X-BTK-SIGN': sig,
        'X-BTK-APIKEY': api_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(host + path, headers=headers, json=reqBody)
        print(response.text)
        return response