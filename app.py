from flask import Flask
from flask import request

import os
import requests
import json
import re
import urllib
import random

import lib.Common as Common

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

API_BASE_URL = os.environ["API_BASE_URL"]
AUTH_BASE_URL = os.environ["AUTH_BASE_URL"]
line_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

app = Flask(__name__)
line_bot_api = LineBotApi(line_token)

static_path = "https://uni-bot-py.herokuapp.com/static"

def getBaseRate(event):
  """
  譜面定数 <曲名>の発言がされたら<曲名>の譜面定数を返す
  """

  match = re.search("^譜面定数\s(.+)", event["message"]["text"])
  music_name = match.group(1)
  encoded = urllib.parse.quote(music_name)
  request_url = API_BASE_URL + "get_baserate/" + encoded
  with urllib.request.urlopen(request_url) as res:
    html = res.read().decode("utf-8")
    ratelist_json = json.loads(html)
    if ratelist_json["items"]:
      if "baserate" in ratelist_json["items"][0]:
        fully_music_name = ratelist_json["items"][0]["music_name"]
        base_rate = ratelist_json["items"][0]["baserate"]
        send_text = fully_music_name + "の譜面定数は " + str(base_rate) + "だよ。"
      else:
        send_text =  "ごめん、その曲は譜面定数はまだわからないみたいだ"

    else:
      send_text = "ごめん、その曲は見つからなかったよ"

    try:
      line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=send_text))
    except LineBotApiError as e:
      print (e)


def daaaa(event):
  send_text = "(チャーーラーラーrーtrwrgwウィmrgtzbダツツダツツダツツダツツダツダツデツツデツツ"
  try:
    line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=send_text))
  except LineBotApiError as e:
    print (e)

def getImage(event):
  match = re.search("^画像\s(.+)", event["message"]["text"])
  image_name = match.group(1)

  cmn = Common.Common()
  image_url_list = cmn.getImageUrl(image_name, 1)

  for image_url in image_url_list:
    try:
      line_bot_api.reply_message(event["replyToken"], ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
    except LineBotApiError as e:
      print (e)
 
def kuma(event):
  send_text = "ぁ？虹レートぞ？敬語使えよ"
  try:
    line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=send_text))
  except LineBotApiError as e:
    print (e)

def responseForStamp(event):

  here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
  image_list = []
  image_url = ""
  # ネガ子ちゃんStamp(1233295)に対するレスポンス
  if event["message"]["packageId"] == "1233295":
    image_list = os.listdir(here + "/static/negami/")
    print (image_list)
    # 「ポチッとな」
    if event["message"]["stickerId"] == "9468023":
      image_list = ["2.png", "4.png", "5.png", "7.png", "9.png"]
 
  image_url = random.choice(image_list)
  try:
    line_bot_api.reply_message(event["replyToken"], ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
  except LineBotApiError as e:
    print (e)

@app.route("/webhook", methods=['POST'])
def webhook():
  """
  Lineからのリクエストをまずこの関数で受け取って送られてきたメッセージに応じて処理を分ける
  """
  req = json.loads(request.get_data(as_text=True))
  for event in req["events"]:
    if "text" in event["message"]:
      if re.match("^譜面定数\s", event["message"]["text"]):
        getBaseRate(event)
      elif re.match("(.*)だー+$", event["message"]["text"]):
        daaaa(event)
      elif re.match("^画像\s", event["message"]["text"]):
        getImage(event)
      elif re.search("くま", event["message"]["text"]):
        kuma(event)
    if event["message"]["type"] == "sticker":
      responseForStamp(event)
  
  return ""

@app.route("/test", methods=['GET'])
def test():
  """
  TEST用
  """
  user_id = "hoge"
  encoded = urllib.parse.quote(user_id)
  url = AUTH_BASE_URL + "get_auth/" + encoded
  with urllib.request.urlopen(url) as res:
    html = res.read().decode("utf-8")
    auth_json = json.loads(html)
    if auth_json["items"]:
      print (auth_json["items"][0]["user_id"])
      print (auth_json["items"][0]["password"])

  return "OK"

@app.route("/", methods=['GET'])
def hogehoge():
  return 'テスト'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(port=port, debug=True)


