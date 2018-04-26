# from flask import Flask, request
# import json
# import requests
# app = Flask(__name__)
# @app.route('/')
# def index():
#   return "Hello World!"

# # ส่วน callback สำหรับ Webhook
# @app.route('/callback', methods=['POST'])
# def callback():
#   json_line = request.get_json()
#   json_line = json.dumps(json_line)
#   decoded = json.loads(json_line)
#   user = decoded["events"][0]['replyToken']
#   #id=[d['replyToken'] for d in user][0]
#   #print(json_line)
#   print("ผู้ใช้：",user)
#   sendText(user,'งง') # ส่งข้อความ งง
#   return '',200


# def sendText(user, text):
#   LINE_API = 'https://api.line.me/v2/bot/message/reply'
#   Authorization = 'Bearer yjTtQCpheReO6VXNVdtDUHmJ8PMU8KOqRSm0Tc9QMb+eaEJD9aa3/tKPL5xAAyPzjfjEHEemUyEO2Pk0pH/0UzqrC7V4Rk7006XwG1FgBjtJSy6re1Ahwa+7wqs8EPI6JWx59n18GgLSGeee3mWBggdB04t89/1O/w1cDnyilFU=' # ใส่ ENTER_ACCESS_TOKEN เข้าไป
#   headers = {
#   'Content-Type': 'application/json; charset=UTF-8',
#   'Authorization':Authorization
#   }
#   data = json.dumps({
#   "replyToken":user,
#   "messages":[{"type":"text","text":text}]})
#   #print("ข้อมูล：",data)
#   r = requests.post(LINE_API, headers=headers, data=data) # ส่งข้อมูล
#   #print(r.text)


# if __name__ == '__main__':
#   app.run(debug=True)
from flask import Flask, request, abort
import json
import requests

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('yjTtQCpheReO6VXNVdtDUHmJ8PMU8KOqRSm0Tc9QMb+eaEJD9aa3/tKPL5xAAyPzjfjEHEemUyEO2Pk0pH/0UzqrC7V4Rk7006XwG1FgBjtJSy6re1Ahwa+7wqs8EPI6JWx59n18GgLSGeee3mWBggdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a1bfdb3d70e30a51c9db71a4f1aacad7')

@app.route('/')
def index():
   return "Hello World!"

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return '', 200

""
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event_hand = event.reply_token
    event_message = event.message.text
    if(event_message == 'สวัสดี'):
        line_bot_api.reply_message(
            event_hand,
            TextSendMessage(text='สวัสดีครับนักศึกษา'))
    else:
        line_bot_api.reply_message(
            event_hand,
            TextSendMessage(text='ขออภัยไม่มีคำสั่งนี้ในฐานข้อมูล'))


if __name__ == "__main__":
    app.run()