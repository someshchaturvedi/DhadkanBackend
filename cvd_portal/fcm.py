import urllib
import os
import json

url = 'https://fcm.googleapis.com/fcm/send'


def send_message(_to, _from, message):
    body = {'to': _to, 'data': message}
    body = json.dumps(body).encode('utf8')
    headers = {
        'content-type': 'application/json',
        'Authorization': 'key=' + os.environ.get('FCM_APIKEY')
        }
    req = urllib.request.Request(
        url, data=body, headers=headers)
    try:
        urllib.request.urlopen(req)
    except:
        pass
