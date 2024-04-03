import os
import json
import httpx
import time
from utils.gen_sign import gen_sign
from dotenv import load_dotenv

load_dotenv()

BITKUB_API_KEY = os.environ.get('BITKUB_API_KEY')
BITKUB_SECRET_KEY = os.environ.get('BITKUB_API_SECRET')

#regarding resolution and acceptable values:
# 1: 1 minute. Each data point represents 1 minute of trading activity.
# 5: 5 minutes. Each data point represents 5 minutes of trading activity.
# 15: 15 minutes. Each data point represents 15 minutes of trading activity.
# 60: 1 hour. Each data point represents 1 hour of trading activity.
# 240: 4 hours. Each data point represents 4 hours of trading activity.
# 1D: 1 day. Each data point represents one day of trading activity.

async def get_chart_data(symbol="SOL_THB", resolution=1, fromDate=None, toDate=None):
    host = 'https://api.bitkub.com'
    path = '/tradingview/history'
    api_key = BITKUB_API_KEY
    api_secret = BITKUB_SECRET_KEY

    if not fromDate:
        fromDate = int(time.time())
    if not toDate:
        toDate = int(time.time())

    reqQuery = {
        'sym': symbol,
        'resolution': resolution,
        'from': fromDate,
        'to': toDate
    }

    ts = str(round(time.time() * 1000))
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
        print(data)
        return response