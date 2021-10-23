from requests import NullHandler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FlexSendMessage,TextSendMessage

import re
import os
from custom_models import onlinePriceComparison, orderCart

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))

def order_cart_flex(event):

    #這行要改成"呼叫購物車"的指令
    if re.match("flex", event.message.text.lower()):
        
        try:

            #get_order_cart_information()目前尚無法取值，請至orderCart.py將資料匯入
            productNameList, productQuantityList, totalMoneyList, index = orderCart.get_order_cart_information()
            contents = orderCart.prepare_flex_orderCart(productNameList, productQuantityList, totalMoneyList, index)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = f'flex 購物車',
                    contents = contents
                )
            )
            
            return True
        
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='flex 購物車 失敗了')
            )
            return False

    else:
        return False



#線上比價的UI沒寫完，不要使用這個
def online_price_comparison_flex(event):
    
    if re.match("flex", event.message.text.lower()):
        
        try:
            
            nameList, priceList, urlList, firstDataIndex, lastDataIndex = function()
            contents = orderCart.prepare_flex_online_price_comparison(
                nameList, priceList, urlList, firstDataIndex, lastDataIndex)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = f'flex 線上比價',
                    contents = contents
                )
            )
            
            return True
        
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='flex 線上比價 失敗了')
            )
            return False

    else:
        return False
