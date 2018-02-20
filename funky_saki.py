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
    saki_detail = requests.get(
        "https://slack.com/api/bots.info", params=payload).json()
    print(saki_detail)
    saki_icon = saki_detail['bot']['icons']['image_48']
    print(saki_icon)   
    #saki_icon = saki_icon['icons']
    # print(saki_icon)
    # return (slack_token, saki_bot_id, saki_icon)
    return (slack_token, saki_bot_id)

# 紗希ちゃんログイン

    
    #return(successedlogin)

# def saki_login():
#     slack_token, saki_bot_id = initbotsetup()

#     try:
#      loginreslt = SlackClient(slack_token)
#      successedlogin = loginreslt.rtm_connect()
#     except:
#          print("OMG failed to slack server! check your code!!")         
#          return

#紗希ちゃんSlackを読む
def saki_readslack():
    # try:
    slack_token, saki_bot_id = initbotsetup()
    sc = SlackClient(slack_token)
    try:
        sc.rtm_connect()
    except:
        return
    #  print  (loginreslt)
    # except:
    #     print("OMG failed connect to slack server! check your code!!(validation err)")
    #     return
    print("loginreslt is ok")  
    while True:
        time.sleep(1)
        rtm_read_jsondata=None
        rtm_read_jsondata = sc.rtm_read()
        #print(rtm_read_jsondata)
        if rtm_read_jsondata == []:
            time.sleep(1)
            #print(rtm_read_jsondata)
            print('nodata!')
            time.sleep(1)
            pass 
        #初期の疎通確認応答やtypingならループ
        else:
                if rtm_read_jsondata[0]['type'] in ['hello','user_typing']:
                        #time.sleep(2)
                        print("loop now(hello)")
                        pass
                else: 
                    print('rtm_read_jsondata')
                    print(rtm_read_jsondata[0]['type'])
                    #typeが message の時にいったん 抜けて チャンネルと 投稿されたメッセージを渡す
                    #rcv_msg_stat = rtm_read_jsondata[0]['type']
                    print(rtm_read_jsondata[0]['user'])
                    # print(rtm_read_jsondata[0]['name'])
                    if rtm_read_jsondata[0]['user'] == 'U8SLQ2932':
                        saki_readslack()
                    else:
                        print(rtm_read_jsondata)
                        print(rtm_read_jsondata[0]['text'])
                        #postsmessage(rtm_read_jsondata[0]['text'])
                        splitmessages(rtm_read_jsondata[0]['text'])
                        saki_readslack()
                            
                        #rcv_msg_username = rtm_read_jsondata[0]['name']
                        #except(KeyError,TypeError):
                            

                        # if rtm_read_jsondata[0]['type'] == 'message' and "name" in rtm_read_jsondata[0]:
                        #     saki_readslack()
                        # else:
                        #     print(rtm_read_jsondata)
                        #     print(rtm_read_jsondata[0]['text'])
                        #     postsmessage(rtm_read_jsondata[0]['text'])


    #紗希ちゃんが読んだメッセージを分割して
    #命令とキーワードに分ける
def splitmessages(message):
    split_msg = message.split()
    if split_msg[0]=="$books" or split_msg[0]=="＄Books":
       search_book(split_msg[1])
    #print(message)
    #print(split_msg[0])
   



# 本検索機能

def search_book(message):
    #print(message.body)
    # スレッドから最新”Books:”の含まれるメッセージを引っ張てくる。
    #  search_word = message.body['text'].split()
    #print(search_word[1])

    # 楽天APIを使って、本のタイトルを検索するよ
    # PayloadはAPIに投げるGetリクエストの内容を定義するよ
    # 検索のトップに出てくるものを結果として出力するよ
    # 参照：https://webservice.rakuten.co.jp/api/booksbooksearch/
    #RAKUtenAIPKeyを実際のトークンに差し替える

    payload = {'applicationId': 'RAKUtenAIPKey',
               'format': 'json',
               'formatVersion': '2',
               'title': message,
               'hits': '1', 'page': '1'}
    try:
        res = requests.get('https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?',
                           params=payload).json()
        #  res = requests.get('',
        #                    params=payload).json()
    except:
        print("Err", sys.exc_info()[0])
        #postsmessage("Err", sys.exc_info()[0])
        return

# 検索結果が見つからない時
    if res['count'] == 0:
        postsmessage("該当する結果が見つかりませんでした")
        return


# 検索結果を各変数に格納する
    result = res['Items'][0]
    result_title = result['title'] + " " + result['subTitle']
    result_author = result['author']
    result_publisher = result['publisherName']
    result_sale = result['salesDate']
    #resultprise = result['itemPrice']
    result_itemurl = result['itemUrl']
    #resultImagepath = result['largeImageUrl']

    print(result)

    postsmessage(result_title)
    postsmessage(result_author)
    postsmessage(result_publisher)
    postsmessage(result_sale)
    # message.send(resultImagepath)
    postsmessage("楽天で見る" + result_itemurl)
    

    

    # else:
    #     print("OMG failed connect to slack server! check your code!!(faild conn slack srv )")
    #     time.sleep(3)
    #     # print(data)
    #     # print(data[0]['type'])
    #     return 0
    # sendmess = str('err')
    # postsmessage(sendmess)
    # return




# def apilogin():


# def getconvers()
#     slack_token, saki_bot_id = initbotsetup()
#     rescall = SlackClient(slack_token)
#     rescall.rtm_send_message():


def postsmessage(message):
    """
    テスト投稿
    """
    #slack_token, saki_bot_id, saki_icon = initbotsetup()
    slack_token, saki_bot_id = initbotsetup()
    rescall = SlackClient(slack_token)
    try:
       rescall.api_call("chat.postMessage",
                     channel="#tech",
                     as_user="true",
                     username="紗希ちゃん",
                     text=message,
                     )
       print(rescall)
    except:
          print(rescall)
          return 1
    return 0


# チャンネルのスレッド一覧を取得する。



