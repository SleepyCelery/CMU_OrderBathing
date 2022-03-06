import json
import os
from typing import List

'''
user.json
----------
{
    'users':
        [
            {'nfine_loginuserkey_2016':'content_1'},
            {'nfine_loginuserkey_2016':'content_2'},
            ......
        ]
}
'''


def clear_users():
    with open('user.json', mode='w') as jsonfile:
        json.dump({'users': []}, jsonfile)


def load_users() -> list:
    if os.path.exists('user.json'):
        with open('user.json', mode='r') as jsonfile:
            return json.load(jsonfile)['users']
    else:
        return []


def dump_users(user_cookies: List[dict]) -> None:
    with open('user.json', mode='w') as jsonfile:
        json.dump({'users': user_cookies}, jsonfile)


def add_user(cookie: dict):
    users = load_users()
    users.append(cookie)
    dump_users(users)


def del_user(cookie: dict):
    users = load_users()
    users.remove(cookie)
    dump_users(users)


def if_exist_user(cookie: dict) -> bool:
    users = load_users()
    if cookie in users:
        return True
    return False
