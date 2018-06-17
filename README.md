# maltego_training

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
    3. defaultはpaterva.comが表示される。アイコンを右クリック -> All Transforms -> To DNS Name Interesting
        - たまに再生ボタンを押下しないと実行されない。
        - DBにすでに登録があったエンティティ（サブドメイン）がにょきにょきでる。
    4. 出てきたサブドメインをドラッグですべて選択し、右クリックしてAll Transforms -> To IP Address
        - それぞれのサブドメインが全て名前解決される。（paterva.comは結局一つのIPに集約されている）
      
    paterva.comがいくつかのサブドメインを持つことそれらのIPアドレスが一つのIPであることを確認できた。
    Maltegoが半自動でサイト間の関係性を可視化したことを確認する。
# 様々なTransform(OSINTの為に便利な情報源)
    - Transform Hub <https://www.paterva.com/web7/about/hub.php>
    - Shodanなど商用データベースなどもある。
    - **syakesabaメモ: Kaggleで公開された匿名化されたデータではなく、プライベートに紐付けられる情報が多いので取扱い注意**
    - 自分でTransformを作ることで、対象組織に特化したOSINTをすることができる
# MaltegoでTransformを自分で作るための最初の一歩
    1. 

## NEM APIに関する注意
    - 今回スクリプトの実行環境: Python3（Python2だとスクリプトが走らない、多分）
    - 今回スクリプトにハードコードされているNEMのAPIのURI: <http://go.nem.njinja:7890>
    - DoS対策されているので、同一グローバルIPからの多重アクセスはBAN対象になる
        - NEMのAPIのURIは他にもドメインが沢山あるので、動かないときはスクリプトを適時書き換えること。




