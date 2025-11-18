import os
import http.client
import json

from cs2.scrape.cs2_terms import categories

from dotenv import load_dotenv
load_dotenv()

conn = http.client.HTTPSConnection("api.csqaq.com")
TOKEN = os.environ.get("cs_api_token")

def get_weapon_ids(weapon_name):

   returns = []

   def make_request(page_index=1):
      payload = json.dumps({
         "page_index": page_index,
         "page_size": 500,
         "search": weapon_name,
      })
      headers = {
         'ApiToken': TOKEN,
         'Content-Type': 'application/json'
      }
      conn.request("POST", "/api/v1/info/get_good_id", payload, headers)
      res = conn.getresponse()
      data = res.read()
      ret = json.loads(data.decode("utf-8")) 
      if ret['code'] != 200:
         raise Exception(f"API error: {ret['msg']}")
      return ret

   first_ret = make_request()
   returns.extend(list(first_ret['data']['data'].values()))
   total = first_ret['data']['total']
   page_num = total // 500 + (1 if total % 500 > 0 else 0)
   if page_num > 1:
      page_numbers = list(range(2, page_num + 1))
      for page_n in page_numbers:
         next_ret = make_request(page_n)
         returns.extend(list(next_ret['data']['data'].values()))

   return returns

def fetch_and_save_to_file(weapon_name):
   ids = get_weapon_ids(weapon_name)
   os.makedirs("WeaponsID", exist_ok=True)
   filename = os.path.join("WeaponsID", f"{weapon_name}_ids.json")
   with open(filename, 'w') as f:
      json.dump(ids, f, ensure_ascii=False, indent=2)
   print(f"Saved {len(ids)} ids for {weapon_name} to {filename}")

from concurrent.futures import ThreadPoolExecutor, as_completed
from throttle import Throttle

throttler = Throttle(capacity=1, recovery_rate=1)

def throttled_fetch_and_save(weapon_name):
   throttler.wait_consume()
   fetch_and_save_to_file(weapon_name)
with ThreadPoolExecutor(max_workers=5) as executor:
   futures = {executor.submit(throttled_fetch_and_save, weapon): weapon for weapon in categories}
   for future in as_completed(futures):
      future.result()
