#!/usr/bin/env python3
#encoding: utf-8

from MaltegoTransform import *
import requests
import datetime
import json

url = "http://go.nem.ninja:7890/account/transfers/outgoing?address="

def getNemTimestamp(nemTimeStamp):
    nemesisTime = datetime.datetime(2015, 3, 29, 9, 6, 25, 0).timestamp()
    timeStamp = nemTimeStamp + int(nemesisiTime)
    timeStamp = datetime.datetime.fromtimestamp(timeStamp)
    return timeStamp

address_id = sys.argv[1]

res = requests.get(url + address_id)

if res.status_code == 200:
    json_data = json.loads(res.text)
    for recipients in json_data["data"]:
        try:
            me = MaltegoTransform()
            ent = me.addEntity("yourorganization.NEM", recipients['transaction']['recipient'])
        except Exception as e:
            raise Exception(e)

me.returnOutput()
