from requests import request as r
import json

API = 'https://dsc.gg/api'


def request(path, method, headers={}, data={}):
    if path is None: return
    if method == "POST":
        return int(r(method, API + path, json=data, headers=headers).text.split(":")[0])
    if method == "GET":
        return r(method, API + path).json()
   