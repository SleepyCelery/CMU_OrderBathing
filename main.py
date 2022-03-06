import threading
from fastapi import FastAPI
from pydantic import BaseModel
from bathing import BathingItem, watch_bathing
from typing import List
import time
import uvicorn
import user_manager

app = FastAPI()

user_manager.clear_users()


class Item(BaseModel):
    building: int
    floor: int
    cookie: dict
    want_pos: List[int]


@app.post('/OrderBathing')
def orderbathing(item: Item):
    b = BathingItem(item.building, item.floor, item.cookie)
    init_status = b.check_waituse_data()
    if init_status:
        if init_status not in item.want_pos:
            b.cancel_order()
        else:
            return '您已经预约了{}号位，剩余{}过期'.format(init_status, b.calc_remaintime())
    while True:
        b.order_bathing()
        time.sleep(1)
        pos = b.check_waituse_data()
        if pos not in item.want_pos:
            time.sleep(1)
            b.cancel_order()
        else:
            return '已经成功预约到{}号位'.format(b.orderarea)
        time.sleep(1)


@app.post('/WatchBathing')
def watchbathing(item: Item):
    if user_manager.if_exist_user(item.cookie):
        return '我已经在监视了，请不要重复发送请求'
    user_manager.add_user(item.cookie)
    t = threading.Thread(target=watch_bathing, args=(item.building, item.floor, item.cookie, item.want_pos))
    t.start()
    print('Watching Thread Start...')
    return '帮您看住了{}号楼{}层的{}号位，直到您开始洗澡为止'.format(item.building, item.floor, "、".join([str(i) for i in item.want_pos]))


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=7767)
