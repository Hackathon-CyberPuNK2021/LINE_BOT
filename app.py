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
                            ButtonsTemplate,
                            MessageTemplateAction,
                            PostbackEvent,
                            PostbackTemplateAction)
import os

app = Flask(__name__)

line_bot_api = LineBotApi("1656508945")
handler = WebhookHandler("368c3211efa65a6432986479092ce6d3")


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    print(get_message)
    if get_message == 'Hi':
        print('IN')
        reply = TextSendMessage(text='Hi')
        line_bot_api.reply_message(event.reply_token, reply)
