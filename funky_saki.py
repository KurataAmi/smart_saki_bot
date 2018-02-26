# -*- coding: utf-8 -*-

# 設定ファイルを読み込む
import configparser
from slackclient import SlackClient
import requests
#import threading
import time
import sys
import json


def initbotsetup():
    """
    紗希ちゃんbotのパラメータを取得します。
    """
    conffile = configparser.SafeConfigParser()
    conffile.read('./app_settings.py', 'UTF-8')
    print(conffile.get("slack", "SLACK_API_TOKEN"))
    slack_token = conffile.get("slack", "SLACK_API_TOKEN")
    saki_bot_id = conffile.get("slack", "SAKI_BOT_ID")
    # Getするパラメータの格納
    payload = {'token': slack_token, 'bot': saki_bot_id}
    # sakiのディティールを取得
    # sakiの情報を取得アイコンなど
#ここで接続エラーのエスケープを入れないと！
    saki_detail = requests.get(
        "https://slack.com/api/bots.info", params=payload).json()
    print(saki_detail)
    saki_icon = saki_detail['bot']['icons']['image_48']
    print(saki_icon)
    #saki_icon = saki_icon['icons']
    # print(saki_icon)
    # return (slack_token, saki_bot_id, saki_icon)
    return (slack_token, saki_bot_id)


# 紗希ちゃんSlackを読む
def saki_readslack():
    slack_token, saki_bot_id = initbotsetup()
    sc = SlackClient(slack_token)
    try:
        sc.rtm_connect()
    except:
        print("OMG failed connect to slack server! check your code!!(validation err)")
        saki_readslack()

    print("loginreslt is ok")
    while True:
        time.sleep(1)
        rtm_read_jsondata = None
        rtm_read_jsondata = sc.rtm_read()
        if rtm_read_jsondata == []:
            time.sleep(1)
            print('nodata!')
            time.sleep(1)
            pass
        # 初期の疎通確認応答やtypingならループ
        else:
            if rtm_read_jsondata[0]['type'] in ['hello', 'user_typing']:
                print("loop now(hello)")
            else:
                print('rtm_read_jsondata')
                print(rtm_read_jsondata[0]['type'])
                try:
                    userid = rtm_read_jsondata[0]['user']
                    print(userid)
                except:
                    saki_readslack()
                #U8SLQ2932は紗希ちゃんのuserID
                if userid == 'U8SLQ2932':
                    saki_readslack()
                else:
                    print(rtm_read_jsondata)
                    print(rtm_read_jsondata[0]['text'])
                    splitmsg = splitmessages(rtm_read_jsondata[0]['text'])
                    channelID = rtm_read_jsondata[0]['channel']
                    if splitmsg != 0:
                        search_book_result = search_book(splitmsg)
                        print(search_book_result)
                        postsmessage(search_book_result, channelID)
                    saki_readslack()

    # 紗希ちゃんが読んだメッセージを分割して
    # 命令とキーワードに分ける


def splitmessages(message):
    split_msg = message.split()
    if split_msg[0] == "$books" or split_msg[0] == "＄Books":
        return(split_msg[1])
    else:
        return 0

# 本検索機能


def search_book(message):
    # 楽天APIを使って、本のタイトルを検索するよ
    # PayloadはAPIに投げるGetリクエストの内容を定義するよ
    # 検索のトップに出てくるものを結果として出力するよ
    # 参照：https://webservice.rakuten.co.jp/api/booksbooksearch/

    payload = {'applicationId': '1051351458834896793',
               'format': 'json',
               'formatVersion': '2',
               'title': message,
               'hits': '1', 'page': '1'}
    try:
        res = requests.get('https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?',
                           params=payload).json()

    except:
        print("Err", sys.exc_info()[0])
        return

# 検索結果が見つからない時
    if res['count'] == 0:
        search_bookresult = "該当する結果が見つかりませんでした"
        return search_bookresult


# 検索結果を各変数に格納する
    result = res['Items'][0]
    result_title = result['title'] + " " + result['subTitle']
    result_author = result['author']
    result_publisher = result['publisherName']
    result_sale = result['salesDate']
    result_itemurl = result['itemUrl']
    print(result)
    # 本タイトル
    # 著者
    # 出版社
    # 発売日
    # 楽天で見る＋URL
    # 検索結果をまとめて戻り値として返す
    search_book_result = [result_title, result_author,
                          result_publisher, result_sale, "楽天で見る" + result_itemurl]
    search_book_result = '\n'.join(search_book_result)
    return search_book_result


def postsmessage(message, channelID):
    """
    テスト投稿
    """
    slack_token, saki_bot_id = initbotsetup()
    rescall = SlackClient(slack_token)
    try:
        rescall.api_call("chat.postMessage",
                         channel=channelID,
                         as_user="true",
                         username=saki_bot_id,
                         text=message,
                         )
        print(rescall)
    except:
        print(rescall)
        return 1
    return 0
