from flask import Flask
from flask import request

import os
import requests
import json
import re
import urllib
import random
import shutil

import common_lib.Common as Common
import common_lib.uni_common_tools.ChunithmNet as ChunithmNet
import common_lib.priconne_gacha_simulator.GachaSimulation as GachaSimulation
import common_lib.priconne_gacha_simulator.ImageGenerator as ImageGenerator

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

#API_BASE_URL  = os.environ["API_BASE_URL"]
#AUTH_BASE_URL = os.environ["AUTH_BASE_URL"]
#line_token    = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

API_BASE_URL  = os.getenv("API_BASE_URL", "")
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "")
line_token    = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

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
  here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
  image_list = []
  image_list = os.listdir(here + "/static/marika/")
  image_url = static_path + "/marika/" + random.choice(image_list)

  try:
    line_bot_api.reply_message(event["replyToken"], ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
  except LineBotApiError as e:
    print (e)

def responseForStamp(event):

  here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
  image_list = []
  image_url = ""
  # ネガ子ちゃんStamp(1233295)に対するレスポンス
  if event["message"]["packageId"] == "1233295":
    image_list = os.listdir(here + "/static/negami/")
    # 「ポチッとな」
    if event["message"]["stickerId"] == "9468023":
      image_list = ["1.png", "3.png", "4.png", "6.png", "7.png"]
 
  image_url = static_path + "/negami/" + random.choice(image_list)
  print (image_url)
  try:
    line_bot_api.reply_message(event["replyToken"], ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
  except LineBotApiError as e:
    print (e)

def tiqav(event):
  match = re.search("^ちくわ\s(.+)", event["message"]["text"])
  image_name = match.group(1)

  cmn = Common.Common()
  image_url = cmn.getTiqavImageUrl(image_name)

  try:
    line_bot_api.reply_message(event["replyToken"], ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
  except LineBotApiError as e:
    print (e)

def bestRate(event):
  match = re.search("^ベストレート\s(.+)", event["message"]["text"])
  name  = match.group(1)

  send_text = ''
  if name == 'チャット':
    ID   = os.environ['CHUNITHM_MY_ID']
    PASS = os.environ['CHUNITHM_MY_PASS']
    cn   = ChunithmNet.ChunithmNet(ID, PASS)
    best_rate = cn.get_my_best_rate()
    send_text = best_rate
  else:
    send_text = 'そんなやつしらねえ'


  try:
    line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=send_text))
  except LineBotApiError as e:
    print (e)
  

def bestMusic(event):
  match = re.search("^ベスト曲\s(.+)", event["message"]["text"])
  name  = match.group(1)

  send_text = ''
  if name == 'チャット':
    ID   = os.environ['CHUNITHM_MY_ID']
    PASS = os.environ['CHUNITHM_MY_PASS']
    cn   = ChunithmNet.ChunithmNet(ID, PASS)
    best_music = cn.get_my_best_music_list()
    send_text = "\n".join(best_music)
  else:
    send_text = 'そんなやつしらねえ'

  try:
    line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=send_text))
  except LineBotApiError as e:
    print (e)

def kimagureMarinka(event):
  num = random.randint(0, 100)

  if num == 0:
    here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
    image_list = []
    image_list = os.listdir(here + "/static/marika/")
    image_url = static_path + "/marika/" + random.choice(image_list)

    try:
      line_bot_api.reply_message(event["replyToken"], ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
    except LineBotApiError as e:
      print (e)
  else:
    print ('not MARINKA!')

def marinka(event):
  genkai_list = ['チャット', 'ステイル', ' だいなむ', 'くま', 'おかわり']
  send_text = random.choice(genkai_list) + 'さん、好き///'
  try:
    line_bot_api.reply_message(event["replyToken"], TextSendMessage(text=send_text))
  except LineBotApiError as e:
    print (e)

def priconneGacha(event):
  gs = GachaSimulation.GachaSimulation()
  charactor_list = gs.roll10()

  ig = ImageGenerator.ImageGenerator()
  gacha_result_path = ig.gacha_result_generator(charactor_list)

  here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
  static_dir = here + "/static/"

  filename = random.random()
  shutil.move(gacha_result_path, static_dir + str(filename))

  image_url = static_path + '/' + str(filename)

  try:
    line_bot_api.reply_message(event["replyToken"], ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
  except LineBotApiError as e:
     print (e)


def priconneYabai(event):
  here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
  image_list = []
  image_list = os.listdir(here + "/static/priconne/")
  # 0.png:「やばいですね」スタンプ
  image_url = static_path + "/priconne/0.png"

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
      elif re.search("ちくわ\s", event["message"]["text"]):
        tiqav(event)
      elif re.search("ベストレート\s", event["message"]["text"]):
        bestRate(event)
      elif re.search("ベスト曲\s", event["message"]["text"]):
        bestMusic(event)
      elif re.search("プリコネ\sガチャ", event["message"]["text"]):
        priconneGacha(event)
      elif re.search("やばい", event["message"]["text"]):
        priconneYabai(event)
#      elif re.search("まりんか", event["message"]["text"]):
#        marinka(event)
      else:
        kimagureMarinka(event)
    if event["message"]["type"] == "sticker":
      responseForStamp(event)
  
  return ""

@app.route("/local_test", methods=['GET'])
def local_test():
  """
  herokuにデプロイする前にローカルでテストしたいとき用
  http://localhost:4000/local_test?param=hogehoge  みたいな感じでアクセス
  """
  param = request.args.get('param')

  event = {}
  event["message"] = {}
  event["message"]["text"] = param
  if re.match("^譜面定数\s", param):
    getBaseRate(event)
  elif re.match("(.*)だー+$", param):
    daaaa(event)
  elif re.match("^画像\s", param):
    getImage(event)
  elif re.search("くま", param):
    kuma(event)
  elif re.search("ちくわ\s", param):
    tiqav(event)
  elif re.search("ベストレート\s", param):
    bestRate(event)
  elif re.search("ベスト曲\s", param):
    bestMusic(event)
  elif re.search("プリコネ\sガチャ", param):
    priconneGacha(event)


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


