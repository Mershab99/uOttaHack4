import json
import os

import requests

os.environ['BACKEND_API_URL'] = "http://35.202.241.3:8000"


def status():
    url = os.environ['BACKEND_API_URL'] + "/status/"
    res = requests.get(url)
    return res.json()


def post_data(event_data, endpoint):
    url = os.environ['BACKEND_API_URL'] + endpoint
    res = requests.post(url, data=event_data)
    return res


def get_settings():
    url = os.environ['BACKEND_API_URL'] + "/settings-get/"
    res = requests.get(url)
    return res.json()


print(status())
print(get_settings())