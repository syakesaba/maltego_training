#!/usr/bin/env python3
#encoding: utf-8

import requests
import json

url = "http://go.nem.ninja:7890/account/transfers/outgoing?address=NBZMQO7ZPBYNBDUR7F75MAKA2S3DHDCIFG775N3D"

response = requests.get(url)
json_data = json.loads(response.text)

for recipients in json_data["data"]:
    print(recipients["transaction"]["recipient"])
