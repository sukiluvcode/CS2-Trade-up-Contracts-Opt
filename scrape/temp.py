import requests

url = "https://api.youpin898.com/api/homepage/pc/goods/market/queryOnSaleCommodityList"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "App-Version": "5.26.0",
    "appType": "1",
    "AppVersion": "5.26.0",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzYzRkNzA4OTMzOWI0NjIxYjM3ODFkMzYwMmY1YzI0ZiIsIm5hbWVpZCI6IjEyNDgzOTM2IiwiSWQiOiIxMjQ4MzkzNiIsInVuaXF1ZV9uYW1lIjoiWVAwMDEyNDgzOTM2IiwiTmFtZSI6IllQMDAxMjQ4MzkzNiIsInZlcnNpb24iOiJCZHQiLCJuYmYiOjE3NTk1NzEwNTksImV4cCI6MTc2MDQzNTA1OSwiaXNzIjoieW91cGluODk4LmNvbSIsImRldmljZUlkIjoiZDYxODg5NDktMTMyOS00OWM1LTk0MDItYjM5MzczNTAxODdhIiwiYXVkIjoidXNlciJ9.jvRy_r9IwVVFZ4cKeby2pak_PoNOODPZcDpxHgqZL6c",
    "b3": "31e83c302b8448c3ab8b796985e2bb32-a55885ca44ac76ef-1",
    "Connection": "keep-alive",
    "Content-Length": "110",
    "Content-Type": "application/json",
    "deviceId": "d6188949-1329-49c5-9402-b3937350187a",
    "deviceUk": "5FRUdYMsbYNOs1O5eSC0dK10xaXhvidAHd8lyMQq5QT1r6UCjdeEHyoi7WOIyRJ1J",
    "Origin": "https://www.youpin898.com",
    "platform": "pc",
    "Priority": "u=3, i",
    "Referer": "https://www.youpin898.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "secret-v": "h5_v1",
    "traceparent": "00-31e83c302b8448c3ab8b796985e2bb32-a55885ca44ac76ef-01",
    "tracestate": "rum=v2&browser&hwztx6svg3@74450dd02fdbfcd&dd7f06fa080942f4ab3352a54cbad18f&uid_8zh1cgt14gs21ivr",
    "uk": "5FPvdY1Uz7YeSw7KA6w3EiTRqOdQXcaxzqWQhyidxBEfm0Vu7AzV9U4rhV1Hz5h1L",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15"
}

with requests.Session() as session:
    payload = {
        "gameId": "730",
        "listType": "10",
        "templateId": "3795",
        "listSortType": 1,
        "sortType": 0,
        "pageIndex": 1,
        "pageSize": 10
    }
    response = session.post(url, json=payload, headers=headers)
    print(response.text)
