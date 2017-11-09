import urllib.request
from urllib.parse import quote
import httplib2
import json
import re
import os, sys

class Common():
  def getImageUrl(self, search_item, total_num):
    GOOGLE_SEACH_API_KEY = os.environ["GOOGLE_SEACH_API_KEY"]
    CUSTOM_SEARCH_ENGINE = os.environ["CUSTOM_SEARCH_ENGINE"]

    img_list = []
    i = 0
    query_img = "https://www.googleapis.com/customsearch/v1?key=" + GOOGLE_SEACH_API_KEY + "&cx=" + CUSTOM_SEARCH_ENGINE + "&num=10&start=" + str(i+1) + "&q=" + quote(search_item) + "&searchType=image"
    #query_img = "https://www.googleapis.com/customsearch/v1?key=" + GOOGLE_SEACH_API_KEY + "&cx=" + CUSTOM_SEARCH_ENGINE + "&num=" + str(10 if(total_num-i)>10 else (total_num-i)) + "&start=" + str(i+1) + "&q=" + quote(search_item) + "&searchType=image"
    res = urllib.request.urlopen(query_img)
    data = json.loads(res.read().decode('utf-8'))
    for j in range(len(data["items"])):
      if re.search('https', data["items"][j]["link"]):
        img_list.append(data["items"][j]["link"])
        break

    return img_list


if __name__ == "__main__":
  args = sys.argv
  common = Common()
  img_dict = common.getImageUrl(args[1], 1)
  print(img_dict)
