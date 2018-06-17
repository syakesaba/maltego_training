# maltego_training
    - 2018.06.17 #tktksec 第8回
    - https://tktksec.connpass.com/
# 攻撃のための情報収集
## OSINT(Open-source intelligence)
    - Open-source intelligence (OSINT) is data collected from publicly available sources to be used in an intelligence context. In the intelligence community, the term "open" refers to overt, publicly available sources (as opposed to covert or clandestine sources).
    - ターゲットの公的な情報を収集する手法（WebInt/特定行動）
    - 例: WHOIS,IP,DNS,関連会社,従業員のユーザ名,メールアドレス,SNSアカウント,創業者,生産製品,生産製品の問い合わせ窓口,雇用対象
### 例:WHOIS
    - ドメイン組織,ドメイン登録組織,事業者,メールアドレス,ネームサーバ,メールサーバ
    - BGP-AS番号（NIC情報）
# Maltego
    - Entity: 情報の単位
    - Transform: 情報を別の情報に変換すること
# Maltegoの実行
    - 実行環境: Kali amd64 2018.02 Maltego 4.1Kali Edition
    - Maltego起動→Maltego CEをクリック
    - Community Editionのアカウント作成(無料、要メールアドレスアクティベーション)
        - https://redirect.paterva.com/maltego/redirect/m3ceregister
    - 取得したアカウントでログイン
## Maltego最初の一歩
    1. 左上のちっちゃい[+]からキャンバスをNew。
    2. 左のペインのEntity -> DomainをキャンバスにDD。
    3. defaultは[paterva.com](paterva.com)が表示される。アイコンを右クリック -> All Transforms -> To DNS Name Interesting
        - たまに再生ボタンを押下しないと実行されない。
        - DBにすでに登録があったエンティティ（サブドメイン）がにょきにょきでる。
    4. 出てきたサブドメインをドラッグですべて選択し、右クリックしてAll Transforms -> To IP Address
        - それぞれのサブドメインが全て名前解決される。（paterva.comは結局一つのIPに集約されている）
      
    paterva.comがいくつかのサブドメインを持つことそれらのIPアドレスが一つのIPであることを確認できた。
    Maltegoが半自動でサイト間の関係性を可視化したことを確認する。
# 様々なTransform(OSINTの為に便利な情報源)
    - Transform Hub: https://www.paterva.com/web7/about/hub.php
    - Shodanなど商用データベースなどもある。
    - メモ: Kaggleで公開された匿名化されたデータではなく、プライベートに紐付けられる情報が多いので取扱い注意
    - 自分でTransformを作ることで、対象組織に特化したOSINTをすることができる
    - MaltegoのTransformを作るPythonバインディングライブラリ: https://github.com/cmlh/MaltegoTransform-Python
        - Python3用: https://github.com/nenaiko-dareda/maltego_training/blob/master/MaltegoTransform.py
# NEMについて
    - 富豪ランキングのお財布: https://nemnodes.org/richlist/
    - コインチェックの2000万XEM(約580億円)送り先: NC4C6PSUW5CLTDT5SXAGJDQJGZNESKFK5MCN77OG
    - XEM-USD Rate: https://www.coingecko.com/en/price_charts/nem/usd
## NEM API叩く際の注意
    - NEM APIの仕様: https://nemproject.github.io/
    - NEM Core API: http://nem-core-api.readthedocs.io/api/
    - 今回スクリプトの実行環境: Python3（Python2だとスクリプトが走らない、多分）
    - 今回スクリプトにハードコードされているNEMのAPIのURI: http://go.nem.njinja:7890/
    - DoS対策されているので、同一グローバルIPからの多重アクセスはBAN対象になる。
        - NEMのAPIのURIは他にもドメインが沢山あるので、動かないときはスクリプトを適時書き換えること。
    - NEMのAPIのTimeStampは「sec from NEM created time」という独自フォーマットになるので注意。
# MaltegoでTransformを自分で作るための最初の一歩
## 写経
### test-maltego.pdf: Maltego形式に変換するスクリプト
```python
#!/usr/bin/env python3
#encoding: utf-8

from MaltegoTransform import *
me = MaltegoTransform()
me.addEntity("maltego.Phrase", "hello world")
me.returnOutput()
```
### test1.pdf: PythonでWebのGET
```python
#!/usr/bin/env python3
#encoding: utf-8

import requests

url = "http://www.yahoo.co.jp"

response = requests.get(url)
print(response.text)
```
### test2.pdf: NEMのAPIから生のJSONをGET
```python
#!/usr/bin/env python3
#encoding: utf-8

import requests

url = "http://go.nem.ninja:7890/account/transfers/outgoing?address=NBZMQO7ZPBYNBDUR7F75MAKA2S3DHDCIFG775N3D"

response = requests.get(url)
print(response.text)
```
### test3.pdf: NEMのAPIから得たJSONを読みやすく整形
```python
#!/usr/bin/env python3
#encoding: utf-8

import requests
import json

url = "http://go.nem.ninja:7890/account/transfers/outgoing?address=NBZMQO7ZPBYNBDUR7F75MAKA2S3DHDCIFG775N3D"

response = requests.get(url)
json_data = json.loads(response.text)
print(json.dumps(json_data, indent=4))
```
### test4.pdf: JSONからrecipients(送信先)のアドレスを抜き出し列挙する
```python
#!/usr/bin/env python3
#encoding: utf-8

import requests
import json

url = "http://go.nem.ninja:7890/account/transfers/outgoing?address=NBZMQO7ZPBYNBDUR7F75MAKA2S3DHDCIFG775N3D"

response = requests.get(url)
json_data = json.loads(response.text)

for recipients in json_data["data"]:
    print(recipients["transaction"]["recipient"])
```
### nem-test1.pdf: 得た情報をMaltego Transform
```python
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
            ent = me.addEntity("youroeganization.NEM, recipients['transaction']['recipient']")
        except:
            pass

me.returnOutput()
```
## 適当なEntityを作ろう！
    1. NEMのアイコンをDL: https://bit.ly/2qM0Rsm (https://www.iconfinder.com/icons/2844392/nem_nemcoin_icon#size=256)
    2. Entities -> New Entity Type
        - Display Name: NEM
        - icons: browse -> manage -> [+] -> アイコンをアップロード
    3. アイコン（small,large）が入ったことを確認する
    4. [step2]はスルー
    5. 最後[step3]はPersonalを選択
    6. うまくいけばEntity Paletteに「NEM」というアイコンが出てくる。
## 適当なTransformを作ろう！
    1. Transforms -> New Local Transforms
        - DisplayName:test
        - Input entity type:Domain
    2. Commandline
        - Command: /usr/bin/python3
        - Parameters: test-maltego.py
        - Working Directory: /root/maltego_training
    3. 適当なDomainエンティティ右クリックして、test Transformsを実行。なんか出たら成功。
# NEMの送信先調査をしよう！
## NEM Transform(送信先羅列Transformを作る)を作ろう！
    1. Transforms -> New Local Transforms
        - DisplayName: NEM
        - Input entity type: NEM
    2. Commanline
        - Command: /usr/bin/python3
        - Parameters: nem-test1.py
        - Working Directory: /root/maltego_training
## NEM Transformをしよう！
    1. NEMエンティティを作る。ダブルクリックをし、NEMアドレスを入れる
    2. NEMエンティティを右クリックし、NEMを選んでTransformする
# ここまでで生成したグラフ
![icons/end.png](icons/end.png)
# 上級者向け
    1. addAdditionalFields()を使って送金金額を追加しなさい。
    2. setLinkLabel()を使って送信日時を矢印に追加しなさい。
## 1. addAdditionalFields()を使って送金金額を追加しなさい。
    1. test3.pyを使って、json構造を見る。（jsonq使った方が良いかも）
    2. ["data"]["transaction"]["timeStamp"]にあることを確認
```javascript
    "data": [
        {
            "meta": {
                "innerHash": {},
                "hash": {
                    "data": "44d740e019e3cba4697c04ab3f417b27c4486ba992ede47dcd527c8ee2ac66b5"
                },
                "id": 2217778,
                "height": 1678714
            },
            "transaction": {
                "fee": 4250000,
                "timeStamp": 101628479,
                "signature": "451a3c5b2cc9a48e043174bac5384b5557f05082f009a7f9d469b7f568db6ffbbf65229dbf0a0ef75c304145b0ea428bac3412016bd11d349290f22e0822e401",
                "amount": 1684187333,
                "version": 1744830465,
                "deadline": 101635679,
                "type": 257,
                "signer": "2f69c71a7cd584e5f92ff787fb1d68aab53985c577eff6e9061c15768899433c",
                "message": {
                    "type": 1,
                    "payload": "313037313536343530"
                },
                "recipient": "NC64UFOWRO6AVMWFV2BFX2NT6W2GURK2EOX6FFMZ"
            }
        },
        {
            "meta": {
                "innerHash": {},
                "hash": {
                    "data": "a8cddcb36bea9fab536c6d31beba5f2ac394845fe5701bc33d1672cb6e5e16ff"
                },
                "id": 2217698,
                "height": 1678661
            },
            "transaction": {
                "fee": 35704549,
                "timeStamp": 101625413,
                "signature": "1185599831f9e12e4dc4343fd20c496262eb97fde989c71badab95102ea352321602b65fa38d20911a9071c917ad5bb46055c9d9fceb6df0d4bd45fd74e53705",
                "amount": 53136490000,
                "version": 1744830465,
                "deadline": 101632613,
                "type": 257,
                "signer": "2f69c71a7cd584e5f92ff787fb1d68aab53985c577eff6e9061c15768899433c",
                "message": {
                    "type": 1,
                    "payload": "36363639"
                },
                "recipient": "NCYAVMNQOZ3MZETEBD34ACMAX3S57WUSWAZWY3DW"
            }
        },
...
    3. 途中！
  

## 2. setLinkLabel()を使って送信日時を矢印に追加しなさい。
    1. 途中
