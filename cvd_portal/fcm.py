import requests
# import os
import json

url = 'https://fcm.googleapis.com/fcm/send'


def send_message(_to, _from, message):
    body = {'to': _to, 'data': {"message": message}}
    body = json.dumps(body).encode('utf8')
    headers = {
        'content-type': 'application/json',
        'Authorization': 'key=' + ''
        }
    r = requests.post(url, data=body, headers=headers)
    print(r.text)
