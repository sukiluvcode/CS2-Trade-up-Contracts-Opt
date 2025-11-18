import os
import http.client
import json
import glob
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

from .throttle import Throttle
from datetime import datetime
from tqdm import tqdm

load_dotenv()
lock = Lock()

throttler = Throttle(capacity=1, recovery_rate=1)
TOKEN = os.environ.get("cs_api_token")
date_str = datetime.now().strftime("%Y-%m-%d")
FILE = f"WeaponsINFO/goods_{date_str}.jsonl"

merged_list = []
json_files = glob.glob("WeaponsID/*.json")
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            merged_list.extend(data)
        else:
            merged_list.append(data)


def fetch_good_info(good_id):
    conn = http.client.HTTPSConnection("api.csqaq.com")
    payload = ''
    headers = {
        'ApiToken': TOKEN
    }
    conn.request("GET", f"/api/v1/info/good?id={good_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded = data.decode("utf-8")
    try:
        ret = json.loads(decoded)
    except json.JSONDecodeError:
        with open("error.log", "a+", encoding="utf-8") as f:
            f.write(f"JSON decode error for good ID {good_id}: {decoded}\n")
        if "Too Many Requests" in decoded:
            throttler.freeze(5)
        return
    if ret.get("code") != 200:
        raise Exception(f"API Error: {ret.get('msg')}")
    with lock:
        with open(FILE, "a+", encoding="utf-8") as f:
            f.write(json.dumps(ret, ensure_ascii=False) + "\n")

def throttled_fetch(good_id):
    throttler.wait_consume()
    fetch_good_info(good_id)

if not os.path.exists(FILE):
    extracted_ids = set()
else:
    with open(FILE, "r", encoding="utf-8") as f:
        f.seek(0)
        extracted_ids = set(json.loads(line.strip())['data']['goods_info']['id'] for line in f.readlines())

with ThreadPoolExecutor(max_workers=5) as executor:
    ids_to_fetch = [item['id'] for item in merged_list if item['id'] not in extracted_ids]
    print(f"Total IDs to fetch: {len(ids_to_fetch)}")
    futures = [executor.submit(throttled_fetch, good_id) for good_id in ids_to_fetch]
    for _ in tqdm(as_completed(futures), total=len(futures), desc="Fetching goods info"):
        pass
