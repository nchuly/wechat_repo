from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
# start_date = os.environ['START_DATE']
start_date = 20220505
# city = os.environ['CITY']
city = "北京"
birthday =  20220505

app_id = 'wx207efee7f1e86bd7'
app_secret = 'dbbaaec490e60dfa890217777d3092ac'

# user_id = ['oxprf6UBve-cxfQ4cQJs7jODfpYA', 'oxprf6W0w1rDmjzs5Z2HJ9YUbQ2Y']
user_id = 'oxprf6UBve-cxfQ4cQJs7jODfpYA'
template_id = 	'xRhUukAj_-P851M3_BCPp-mrn-5dYBDKZyJbWUftUkk'


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
# for id in user_id:
#   res = wm.send_template(id, template_id, data)
#   print(res)