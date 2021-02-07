import os

import requests

os.environ['BACKEND_API_URL'] = "http://35.202.241.3:8000"


def status():
    try:
        url = os.environ['BACKEND_API_URL'] + "/status/"
        res = requests.get(url)
        return res.json()
    except Exception as e:
        print(e)


def post_data(event_data, endpoint):
    try:
        url = os.environ['BACKEND_API_URL'] + endpoint
        res = requests.post(url, data=event_data)
        return res.json()
    except Exception as e:
        print(e)


def get_settings():
    try:
        url = os.environ['BACKEND_API_URL'] + "/settings-get/"
        res = requests.get(url)
        return res.json()
    except Exception as e:
        print(e)

print("API Broker Healthcheck\n")
print(status())
print(get_settings())
