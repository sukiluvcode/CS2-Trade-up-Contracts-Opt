import requests

url = "https://api.youpin898.com/api/homepage/pc/goods/market/queryOnSaleCommodityList"
headers = { "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "uk": "5FPvdY1Uz7YeSw7KA6w3EiTRqOdQXcaxzqWQhyidxBEfm0Vu7AzV9U4rhV1Hz5h1L",
    "Accept-Language": "en-US,en;q=0.9",
    "App-Version": "5.26.0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "secret-v": "h5_v1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
}

template_ids = ["44220"]  # Add all templateIds you need
page_size = 10

with requests.Session() as session:
    session.headers.update(headers)
    for template_id in template_ids:
        print(f"Fetching templateId: {template_id}")
        page_index = 1
        while True:
            payload = {
                "gameId": "730",
                "listType": "10",
                "templateId": template_id,
                "listSortType": 1,
                "sortType": 0,
                "pageIndex": page_index,
                "pageSize": page_size
            }
            response = session.post(url, json=payload)
            data = response.json()
            items = data.get("data", {}).get("items", [])
            print(f"templateId={template_id}, page={page_index}, items={len(items)}")
            print(data)
            break
            if not items:
                break
            page_index += 1