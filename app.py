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

def getBaseRate(music_name):
  line_bot_api = LineBotApi(line_token)

  #encoded_music_name = music_name.encode()
  encoded = urllib.parse.quote(music_name)
  #print (encode)
  request_url = BASE_URL + encoded
  with urllib.request.urlopen(request_url) as res:
    html = res.read().decode("utf-8")
    ratelist_json = json.loads(html)
    if ratelist_json["items"]:
      fully_music_name = ratelist_json["items"][0]["music_name"]
      base_rate = ratelist_json["items"][0]["baserate"]
      try:
        line_bot_api.push_message('1490485307', TextSendMessage(text='fooo'))
      except LineBotApiError as e:
        print ("ERROR")

    else:
      print ("ごめん、その曲は見つからなかったよ")

@app.route("/webhook", methods=['POST'])
def webhook():
  req = request.get_data(as_text=True)
  print (req)
  for event in req:
    reply_token = event["replyToken"]
    try:
      line_bot_api.reply_message(reply_token, TextSendMessage(text='Hello!'))
    except LineBotApiError as e:
      print ("ERROR")
  
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
    #context = ('cert/server.pem', 'cert/privkey.pem')
    port = int(os.environ.get('PORT', 4000))
    app.run(port=port, debug=True)


