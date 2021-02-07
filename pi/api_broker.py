import os
import requests

os.environ['BACKEND_API_URL'] = ""


def post_data(event_data, endpoint):
    url = os.environ['BACKEND_API_URL'] + endpoint
    res = requests.post(url, data=event_data)
    return res
