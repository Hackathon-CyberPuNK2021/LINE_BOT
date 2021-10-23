from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FlexSendMessage,TextSendMessage
import os

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))

seeMoreFlex = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "flex": 1,
            "gravity": "center",
            "action": {
              "type": "postback",
              "label": "瀏覽更多",
              "data": "瀏覽更多商品"
            }
          }
        ]
      }
    }


def prepare_single_flex_online_price_comparison(nameList, priceList, urlList, index):
    contents = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "線上比價",
                            "color": "#1DB446"
                        },
                        {
                            "type": "text",
                            "text": nameList[index],
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"${priceList[index]}",
                                    "weight": "bold",
                                    "size": "xl",
                                    "flex": 0
                                }
                            ]
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
                            "style": "secondary",
                            "action": {
                                "type": "uri",
                                "label": "商品連結",
                                "uri":  urlList[index]
                            }
                        }
                    ]
                }
            }
    return contents

def prepare_mulitiple_flex_online_price_comparison(flexContent):

    contents = {
                "type": "carousel",
                "contents": []
    }
    contents['contents'] = flexContent



    return contents

def prepare_flex_online_price_comparison(nameList, priceList, urlList, firstDataIndex, lastDataIndex):
    flexContent = []
    for index in range(firstDataIndex,lastDataIndex):
        singleContents = prepare_single_flex_online_price_comparison(nameList, priceList, urlList, index)
        flexContent.append(singleContents.copy())
    flexContent.append(seeMoreFlex.copy())
    contents = prepare_mulitiple_flex_online_price_comparison(flexContent)
    return contents