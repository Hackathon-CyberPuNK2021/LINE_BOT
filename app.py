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

line_bot_api = LineBotApi(
    "bUO9INGLyZOOYLdLepMUpcUgbGI0ErNUcedB9pbyZjWBfGDqyUESlQA7UcwQSZZWovH5Dnqj8pg0JuJbCOG68TtqbKG3JOaetLnaH3kLaQ81GMOl95W61WrfhQUdJdEvlYNqETr/0dCLmKjmL85XBQdB04t89/1O/w1cDnyilFU=")
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
    if get_message == 'Hi':
        reply = TextSendMessage(text='Hi')
        line_bot_api.reply_message(event.reply_token, reply)
