#!/usr/bin/env python3
#encoding: utf-8

import requests

url = "http://www.yahoo.co.jp"

response = requests.get(url)
print(response.text)
