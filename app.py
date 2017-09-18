from flask import Flask
from flask import request

import os
import requests
import json
import re
import urllib

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

API_BASE_URL = os.environ["API_BASE_URL"]
AUTH_BASE_URL = os.environ["AUTH_BASE_URL"]
line_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

app = Flask(__name__)
line_bot_api = LineBotApi(line_token)

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
      print ("ERROR")


def daaaa(event):
  send_text = "(チャーーラーラーrーtrwrgwウィmrgtzbダツツダツツダツツダツツダツダツデツツデツツ"
  try:
    line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=send_text))
  except LineBotApiError as e:
    print ("ERROR")

@app.route("/webhook", methods=['POST'])
def webhook():
  """
  Lineからのリクエストをまずこの関数で受け取って送られてきたメッセージに応じて処理を分ける
  """
  req = json.loads(request.get_data(as_text=True))
  for event in req["events"]:
    if re.match("^譜面定数\s", event["message"]["text"]):
      getBaseRate(event)
    elif re.match("(.*)だー+$", event["message"]["text"]):
      daaaa(event)
  
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


