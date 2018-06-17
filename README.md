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
      
    __paterva.comがいくつかのサブドメインを持つことそれらのIPアドレスが一つのIPであることを確認できた。__  
    __Maltegoが半自動でサイト間の関係性を可視化したことを確認する__  


