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
        info = {"mode_off": False, id: info_id}

    if get_message[0] == '#':  # 資料庫搜尋
        get_message = get_message[1:].rstrip().strip()
        content = '您要購買的是 '+get_message
        text_reply(content, event)

    elif get_message[0] == '?' or get_message[0] == '？' or get_message.isdigit():  # 比價用
        mode_off = """機器人目前測試中，請稍後再使用
        輸入help可查詢使用方式及新增功能"""
        Except = """無法搜尋到商品，請確認輸入是否有誤～"""
        start = time.time()
        text = get_message[1:].rstrip().strip()
        id_developer = "U1e38384f12f22c77281ec3e8611025c8"
        if info["mode_off"] and id != id_developer:
            message = mode_off
        elif ";" in text:
            info_id["search_name"], info_id["platform"] = text.split(";")
            message = search(id, info_id)
        elif "；" in text:
            info_id["search_name"], info_id["platform"] = text.split("；")
            message = search(id, info_id)
        elif get_message.isdigit() == True:
            message = search(id, info_id, int(text))
        elif text.isdigit() == True:
            message = search(id, info_id, int(text))
        elif text == "mode off" and id == id_developer:
            info["mode_off"] = True
            print("mode off")
            message = "mode off"
        elif text == "mode on" and id == id_developer:
            info["mode_off"] = False
            print("mode on")
            message = "mode on"
        else:
            message = Except
        with open("search_info.json", "w") as file:
            json.dump(info, file)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
        end = time.time()
        print("time:", end - start, "s")
        pass
    else:
        if get_message.upper()[:2] == 'HI':
            interface = FlexSendMessage(
                alt_text='Hi',  # 在聊天室外面看到的文字訊息
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
                                    "label": "線上比價",
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
        text_reply('請輸入商品關鍵字(請在開頭打「?」 ex: ?耳機、?馬克杯...)：', event)
        pass
    elif data == 'A&func3':
        text_reply(data, event)
    elif data == 'A&func1&func1':
        text = """【搜尋功能】
        若想在 pchome/momo/shopee 搜尋商品
        請輸入：  商品名稱;平台 
        (英文請輸入半型)
        Ex:  PS5;pchome 、 滑鼠；MOMO
        要看下一頁則輸入2 3 4 5....

        【比價功能】
        請輸入： 商品名稱;price1/price2
        (英文請輸入半型)
        price1：從最低價開始排
        price2：從最高價開始排
        Ex:  PS5;price1 、 滑鼠；Price2
        要看下一頁則輸入2 3 4 5....


        【注意】
        pchome回傳時間<3秒
        momo回傳時間<3秒
        shopee回傳時間<4秒
        price回傳時間<6秒

        ------------------------------
        請輸入商品關鍵字(請在開頭打「#」 ex: #耳機、#馬克杯...)：
        """
        text_reply(text, event)
        pass
    elif data == 'A&func1&func2':
        pass

    # text_reply(data, event)
