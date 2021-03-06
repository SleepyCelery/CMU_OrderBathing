import requests
from typing import Union
import time
import re
import user_manager
from loguru import logger

building_table = {
    '1': '0001',
    '2': '0002',
    '3': '0003',
    '4': '0004',
    '5': '0005',
    '6': '0006',
    '7': '0007',
    '8': '0008',
    '9': '0009',
    '10': '0100',
    '11': '0110',
    '12': '0120',
    '13': '0130',
}


class BathingItem:
    def __init__(self, building: Union[int, str], floor: Union[int, str], cookie: dict):
        self.building = building
        self.floor = floor
        self.cookie = cookie
        self.ordered = False
        self.orderarea = ""
        self.orderexpiretime = 0
        self.if_opentab = False

    def check_orderstatus(self):
        current_time = int(time.time() * 1000)
        if current_time > self.orderexpiretime or not self.ordered:
            return False
        return True

    def order_bathing(self):
        headers = {
            'Host': 'intelligence.cmu.edu.cn',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://intelligence.cmu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/4.0.1 MicroMessenger/7.0.1 Language/zh ColorScheme/Dark',
            'Connection': 'keep-alive',
            'Referer': 'http://intelligence.cmu.edu.cn/Bathing/Index',
            'Content-Length': '26',
        }

        data = {
            'areaId': building_table[str(self.building)],
            'orderArea': "{}{}".format(str(self.building), str(self.floor)).zfill(4)
        }

        response = requests.post('http://intelligence.cmu.edu.cn/Bathing/OrderBathing', headers=headers,
                                 cookies=self.cookie, data=data, timeout=15)
        if response.json()['info'] == 'canuse':
            self.ordered = True
            return True
        else:
            self.ordered = False
            return False

    def check_waituse_data(self):
        headers = {
            'Host': 'intelligence.cmu.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://intelligence.cmu.edu.cn',
            'Content-Length': '0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/4.0.1 MicroMessenger/7.0.1 Language/zh ColorScheme/Dark',
            'Referer': 'http://intelligence.cmu.edu.cn/Bathing/WaitUse',
        }

        response = requests.post('http://intelligence.cmu.edu.cn/Bathing/GetWaitUseData', headers=headers,
                                 cookies=self.cookie, timeout=15)
        try:
            data = response.json()
            if data['state'] == 'start':
                self.orderarea = int(re.findall(r'.*???????.*????(.*?)??????', data['data']['orderArea'])[0])
                self.orderexpiretime = int(data['data']['effectiveTime'][6:-2])
                self.if_opentab = False
                return self.orderarea
            elif data['state'] == 'wait':
                self.orderarea = int(re.findall(r'.*???????.*????(.*?)??????', data['data']['orderArea'])[0])
                self.orderexpiretime = int(data['data']['effectiveTime'][6:-2])
                self.if_opentab = True
                return self.orderarea
            else:
                return None
        except:
            return None

    def cancel_order(self):
        if self.ordered:
            headers = {
                'Host': 'intelligence.cmu.edu.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept': '*/*',
                'Origin': 'http://intelligence.cmu.edu.cn',
                'Content-Length': '0',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/4.0.1 MicroMessenger/7.0.1 Language/zh ColorScheme/Dark',
                'Referer': 'http://intelligence.cmu.edu.cn/Bathing/WaitUse',
            }

            response = requests.get('http://intelligence.cmu.edu.cn/Bathing/CancelOrder', headers=headers,
                                    cookies=self.cookie)
            if response.text == 'success':
                self.ordered = False
                return True
            else:
                self.ordered = False
                return False

    def calc_remaintime(self):
        current = int(time.time() * 1000)
        seconds = (self.orderexpiretime - current) // 1000
        if seconds >= 60:
            minutes = seconds // 60
            seconds -= minutes * 60
            return f'{minutes}???{seconds}???'
        else:
            return f'{seconds}???'


def watch_bathing(building, floor, cookie, want_pos):
    b = BathingItem(building, floor, cookie)
    while True:
        try:
            # ????????????????????????????????????
            status = b.check_waituse_data()
            # ?????????????????????????????????
            if not status:
                # ???????????????????????????
                print('????????????{}???{}???{}??????...'.format(building, floor, "???".join([str(i) for i in want_pos])))
                while True:
                    b.order_bathing()
                    time.sleep(2)
                    pos = b.check_waituse_data()
                    if pos not in want_pos:
                        time.sleep(1)
                        b.cancel_order()
                    else:
                        break
            # ?????????????????????????????????,????????????
            elif status and not b.if_opentab:
                print("{}???{}???{}?????????????????????".format(building, floor, b.orderarea))
                time.sleep(5)
                continue
            # ????????????????????????????????????????????????
            elif status and b.if_opentab:
                print('?????????????????????????????????')
                user_manager.del_user(cookie)
                break
            # ???????????????????????????????????????????????????????????????
            elif int(time.strftime('%H%M%S')) <= 5:
                break
        except Exception as e:
            logger.error(e)
            continue
