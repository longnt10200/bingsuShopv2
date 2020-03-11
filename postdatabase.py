import requests
import json

API_ENDPOINT = "http://192.168.4.58:8888/api/v1/ai/customer"

def postdata(data, api = API_ENDPOINT):
    '''
    data struct
    data = {"time": timestamp,
            "count": number,
            "id_store": string}
    '''
    headers = {"Content-Type": "application/json"}
    r = requests.post(url=API_ENDPOINT, data=data, headers=headers)
    pastebin = r.text
    print("[INFO] the pastebin URL is {}".format(pastebin))