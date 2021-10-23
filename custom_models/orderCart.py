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

#刪除data: deleteCartProduct, 下單data: orderCartProduct
def prepare_single_flex_orderCart(productNameList, productQuantityList, totalMoneyList, index):
    contents =    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "購物車",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
          },
          {
            "type": "text",
            "text": productNameList[index],
            "weight": "bold",
            "size": "xl",
            "margin": "md"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "商品名稱",
                    "size": "sm",
                    "flex": 0,
                    "color": "#aaaaaa"
                  },
                  {
                    "type": "text",
                    "text": productNameList[index],
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "購買數量",
                    "size": "sm",
                    "color": "#aaaaaa",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": productQuantityList[index],
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "總共金額",
                    "size": "sm",
                    "color": "#aaaaaa",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "$"+ totalMoneyList[index],
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "postback",
              "data": "deleteCartProduct",
              "label": "刪除"
            },
            "style": "link"
          },
          {
            "type": "button",
            "action": {
              "type": "postback",
              "label": "下單",
              "data": "orderCartProduct"
            },
            "style": "primary"
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return contents

def prepare_mulitiple_flex_orderCart(flexContent):

    contents = {
                "type": "carousel",
                "contents": []
    }
    contents['contents'] = flexContent
    return contents

def prepare_flex_orderCart(productNameList, productQuantityList, totalMoneyList, index):
    flexContent = []
    for index in range(index):
        singleContents = prepare_single_flex_orderCart(productNameList, productQuantityList, totalMoneyList, index)
        flexContent.append(singleContents.copy())
    contents = prepare_mulitiple_flex_orderCart(flexContent)
    return contents

def get_order_cart_information():
    productNameList = []
    productQuantityList = []
    totalMoneyList = []
    index = []
    
    return productNameList, productQuantityList, totalMoneyList, index