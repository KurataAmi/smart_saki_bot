▼コンセプト
    一問一答ではなく自然言語で理解して本を探してきてくれるちょっと気が利く紗希ちゃんBot

▼botのふるまい
    １ユーザーが”本を探したいという”
        1.1Botがメッセージ一覧を取得して”本を探したい”というまでまつ
    ２”タイトル？もしくは著者名からさがす？”とbotが質問する
    ３ユーザーがタイトル？もしくは著者名を回答する。
    ４botが著者名かタイトルで楽天を検索して回答する。
    ５終わり




▼参考URL
    ▼公式ドキュメント
        http://slackapi.github.io/python-slackclient/conversations.html
        https://github.com/slackapi/python-slackclient

▼Bot作成手順
    1   Botが毎回動作するごとに必要なパラメータをどこかに定義して保持する
        APIキーがあればどうにかなるような設計
    2   会話の前後をいい感じに覚えてくれる設計
    3   書物の検索を行って値を返す設計
    4   自然言語でいい感じに解釈してくれる設計




▼ユーザーIDやチャンネルIDを取得する
patarn1 slackclient 使うパターン
    from slackclient import SlackClient

    rescall = slkclt.api_call("chat.postMessage", channel="#tech", username="takamiya_saki", text="Hello from Python!(カンバセーションAPI) :tada:")
    print(rescall)

    rescallの中身
    {'ok': True, 'channel': 'C8707BNP6', 'ts': '1516503606.000031', 'message': {'text': 'Hello from Python!(カンバセーションAPI) :tada:', 'username': 'takamiya_saki', 'bot_id': 'B8T7GGBU3', 'type': 'message', 'subtype': 'bot_message', 'ts': '1516503606.000031'}}


patarn2 requests 使ってWebAPIから拾うパターン
    from requests

        payload = {'applicationId': '1051351458834896793',
                   'format': 'json',
                   'formatVersion': '2',
                    'title': search_word[1],
                    'hits': '1', 'page': '1'}
                    

         res = requests.get('https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?', params=payload).json()


