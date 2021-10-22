from bs4.element import TemplateString
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
    id = event.source.user_id  # 獲取使用者ID
    print(id)
    get_message = event.message.text.rstrip().strip()  # 刪除回應裡左右的多餘空格
    if get_message[0] == '#':
        get_message = get_message[1:].rstrip().strip()
        text_reply(get_message, event)
        pass
    else:
        if get_message.upper()[:2] == 'HI':
            interface = FlexSendMessage(
                alt_text='Hi',  # 在聊天室外面看到的文字訊息
                contents={  # flex介面 到這邊手刻:https://developers.line.biz/flex-simulator/?status=success
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://cdn.unwire.hk/wp-content/uploads/2020/10/1028-1b.jpg",
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
        elif get_message.upper()[:4] == 'help':
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
                        "url": "https://cdn.unwire.hk/wp-content/uploads/2020/10/1028-1b.jpg",
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
        text_reply(data, event)
    elif data == 'A&func3':
        text_reply(data, event)
    elif data == 'A&func1&func1':
        text_reply('請輸入商品關鍵字(請在開頭打「#」 ex: #耳機、#馬克杯...)：', event)
        pass
    elif data == 'A&func1&func2':
        pass

    # text_reply(data, event)
