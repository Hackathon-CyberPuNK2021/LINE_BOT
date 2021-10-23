from bs4.element import ContentMetaAttributeValue, TemplateString
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage,
                            ImageSendMessage,
                            VideoSendMessage,
                            AudioSendMessage,
                            LocationSendMessage,
                            StickerSendMessage,
                            ImagemapSendMessage,
                            TemplateSendMessage,
                            FlexSendMessage,
                            ButtonsTemplate,
                            MessageTemplateAction,
                            PostbackEvent,
                            PostbackTemplateAction)
import os
import random
import json
from linebot.models.flex_message import BubbleStyle
import psycopg2
import requests
import urllib
import contextlib
import time
from urllib.parse import urlencode
from urllib.request import urlopen
from emoji import UNICODE_EMOJI
from bs4 import BeautifulSoup

from online_cmp import*
from trade import*

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


def text_reply(content, event):
    reply = TextSendMessage(text=content)
    line_bot_api.reply_message(event.reply_token, reply)


@handler.add(MessageEvent, message=TextMessage)  # 普通訊息的部分
def handle_message(event):

    DATABASE_URL = os.environ['DATABASE_URL']  # 資料庫區塊
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    with open('user.json', 'r', encoding='utf8') as jfile:  # 識別身分
        jdata = json.load(jfile)
    #file = open(fileName, "w")
    #json.dump(jsonString, file)
    # file.close()

    id = event.source.user_id  # 獲取使用者ID
    print(id)
    get_message = event.message.text.rstrip().strip()  # 刪除回應裡左右的多餘空格

    try:
        with open("search_info.json") as file:
            info = json.load(file)
            try:
                info_id = info[id]
            except:
                info_id = {}
                info[id] = info_id
    except:
        info_id = {}
        info = {id: info_id}

    if get_message[0] in ['?', '？'] or get_message.isdigit():  # 比價用
        start = time.time()
        if get_message[0] in ['?', '？']:
            text = get_message[1:].lower().rstrip().strip()
        else:  # 頁數
            text = get_message
        if ";" in text:
            info_id["search_name"], info_id["platform"] = text.split(";")
            Bubble = search(id, info_id)
        elif "；" in text:
            info_id["search_name"], info_id["platform"] = text.split("；")
            Bubble = search(id, info_id)
        elif text.isdigit() == True:
            Bubble = search(id, info_id, int(text))
        print(info)
        with open("search_info.json", "w") as file:
            json.dump(info, file)
        if Bubble == -1:
            text_reply("無法搜尋到商品，請確認輸入是否有誤～", event)
        else:
            interface = FlexSendMessage(
                alt_text='func2',  # 在聊天室外面看到的文字訊息
                contents=Bubble
            )
            line_bot_api.reply_message(event.reply_token, interface)
        end = time.time()
        print("time:", end - start, "s")
        pass
    elif get_message[:2] == '上架':
        d = updateDictionary(get_message[3:])
        work = d["name"]
        text_reply(work, event)
        # print(type(d))
        id = 886
        try:
            updateMember(id, d, cursor, conn)
        except:
            Except = """輸入錯誤！請按照以下格式
上架:賣家暱稱;電話號碼;商品名稱;商品敘述;圖片網址;價格;商品數量;賣家地區
(ex: 上架:王曉明;0911111450;兔子布偶;可愛ㄉ玩偶;圖片網址;900;1;台北)
            """
            text_reply(Except, event)
        updateProduct(id, d, cursor, conn)
        finish = "上架完成！"
        text_reply(finish, event)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        if get_message.upper()[:2] == 'HI':
            interface = FlexSendMessage(
                alt_text='Hi',  # 在聊天室外面看到的文字訊息
                # flex介面 到這邊手刻:https://developers.line.biz/flex-simulator/?status=success
                contents={
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/pf87Feb.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "action": {
                            "type": "uri",
                            "uri": "http://linecorp.com/"
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "功能選單",
                                "weight": "bold",
                                "size": "xl"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "下單/上架",
                                    "data": "A&func1"
                                },
                                "style": "primary"
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "action": {
                                    "type": "postback",
                                    "label": "線上比價/跨平台搜尋",
                                    "data": "A&func2"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "物流追蹤",
                                    "data": "A&func3"
                                },
                                "style": "secondary"
                            }
                        ],
                        "flex": 0
                    }
                }
            )
            line_bot_api.reply_message(event.reply_token, interface)
        elif get_message.upper()[:4] == 'HELP':
            helpWord = ''
            text_reply(helpWord, event)
        else:
            textList = ['叫出選單的指令是「Hi」喔']  # 看要不要加笑話之類的
            text = random.choice(textList)
            text_reply(text, event)


@handler.add(PostbackEvent)  # Postback的部分
def handle_postback(event):
    id = event.source.user_id
    data = event.postback.data
    if data == 'A&func1':  # 點擊「下單/上架」
        interface = FlexSendMessage(
            alt_text='A&func1',  # 在聊天室外面看到的文字訊息
            contents={  # flex介面 到這邊手刻:https://developers.line.biz/flex-simulator/?status=success
                "type": "bubble",
                "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/pf87Feb.png",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "action": {
                            "type": "uri",
                            "uri": "http://linecorp.com/"
                        }
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "我要下單商品",
                                    "data": "A&func1&func1"
                                }
                            },
                        {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                    "type": "postback",
                                    "label": "我要上架商品",
                                    "data": "A&func1&func2"
                                }
                            },
                        {
                                "type": "spacer",
                                "size": "sm"
                            }
                    ],
                    "flex": 0
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, interface)
    elif data == 'A&func2':
        text = """【比價功能】
請輸入： ?商品名稱;price1/price2
(英文請輸入半型)
price1：從最低價開始排
price2：從最高價開始排
Ex:  PS5;price1 、 滑鼠；Price2
要看下一頁則輸入2 3 4 5....

【搜尋功能】  
若想在 pchome/momo/shopee 搜尋商品
請輸入：  ?商品名稱;平台 
(英文請輸入半型)
Ex:  PS5;pchome 、 滑鼠；MOMO
要看下一頁則輸入2 3 4 5....

------------------------------

【注意】
pchome回傳時間<3秒
momo回傳時間<3秒
shopee回傳時間<4秒
price回傳時間<6秒
        
------------------------------
請輸入商品關鍵字(請在開頭打「?」 ex: ?耳機;shopee、?馬克杯;...)：
        """
        text_reply(text, event)
        pass
    elif data == 'A&func3':
        text_reply(data, event)
    elif data == 'A&func1&func1':
        text = """<下單功能>
        請輸入商品關鍵字(請在開頭打「?」 ex: ?耳機、?馬克杯...)：
        """
        text_reply(text, event)
        pass
    elif data == 'A&func1&func2':
        text = """<上架功能>
請在開頭輸入「上架:」，商品相關資訊依序為:
賣家暱稱;電話號碼;商品名稱;商品敘述;圖片網址;價格;商品數量;賣家地區
(ex: 上架:王曉明;0911111450;兔子布偶;可愛ㄉ玩偶;圖片網址;900;1;台北)
        """
        text_reply(text, event)

    # text_reply(data, event)
# products_info = {id: products, ...}
# products = [{"url": url, "name": name, "price": price}, ...]
