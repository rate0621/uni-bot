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

BASE_URL = 'https://apex.oracle.com/pls/apex/chunithm/chunithm_music/';
line_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

app = Flask(__name__)
line_bot_api = LineBotApi(line_token)

def getBaseRate(event):
  music_name = re.search("^譜面定数\s(.+)", event["message"]["text"])
  encoded = urllib.parse.quote(music_name)
  request_url = BASE_URL + encoded
  with urllib.request.urlopen(request_url) as res:
    html = res.read().decode("utf-8")
    ratelist_json = json.loads(html)
    if ratelist_json["items"]:
      fully_music_name = ratelist_json["items"][0]["music_name"]
      base_rate = ratelist_json["items"][0]["baserate"]
      try:
        line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=fully_music_name + "の譜面定数は " + base_rate + "だよ。" ))
      except LineBotApiError as e:
        print ("ERROR")
    else:
      print ("ごめん、その曲は見つからなかったよ")

@app.route("/webhook", methods=['POST'])
def webhook():
  req = json.loads(request.get_data(as_text=True))
  for event in req["events"]:
    if re.match("^譜面定数\s", event["message"]["text"]):
      getBaseRate(event)
    reply_token = event["replyToken"]
    try:
      line_bot_api.reply_message(reply_token, TextSendMessage(text='Hello!'))
    except LineBotApiError as e:
      print ("ERROR")
  
  return ""
  #body = request.get_data(as_text=True)
  #print 

@app.route("/", methods=['GET'])
def test():
  return 'テスト'
#    hoge = request.args.get('hoge', '')
#    match = re.search("^譜面定数\s(.+)", hoge)
#    if match:
#      music_name = match.group(1)
#      getBaseRate(music_name)
#      return "OK"
#    else:
#      return "NG"
#    #return '<h1> test </h1>'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(port=port, debug=True)


