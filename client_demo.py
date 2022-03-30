import requests
from typing import List

ORDER_URL = "http://127.0.0.1:7767/OrderBathing"
WATCH_URL = "http://127.0.0.1:7767/WatchBathing"


# 单次预约
def order_bathing(building: int, floor: int, cookie: dict, want_pos: List[int]):
    for i in want_pos:
        assert 1 <= i <= 6
    json_data = {
        "building": building,
        "floor": floor,
        "cookie": cookie,
        "want_pos": want_pos
    }
    response = requests.post(url=ORDER_URL, json=json_data)
    print(response.text)


# 监视位置（持续预约）
def watch_bathing(building: int, floor: int, cookie: dict, want_pos: List[int]):
    for i in want_pos:
        assert 1 <= i <= 6
    json_data = {
        "building": building,
        "floor": floor,
        "cookie": cookie,
        "want_pos": want_pos
    }
    response = requests.post(url=WATCH_URL, json=json_data)
    print(response.text)


if __name__ == '__main__':
    building = 13
    floor = 5
    cookie = {"nfine_loginuserkey_2016": "xxxxxxxxxx"}
    want_pos = [2]
    watch_bathing(building, floor, cookie, want_pos)
