# coding:utf-8
import time
import zxing
from socket import*
from email.mime.text import MIMEText
from random import*
import smtplib
import requests
import json
import platform
import sys
import urllib.request ,re,os
import time
from re import*
import requests
from urllib.request import*
import json
def baidubaike(text):
    html=urllib.request.urlopen("http://gop.asunc.cn/baike.html").read().decode("utf-8")
    url=html+urllib.parse.quote(text)
    html=urllib.request.urlopen(url).read().decode("utf-8")
    par = '(<meta name="description" content=")(.*?)(">)'
    try:
        data = re.search(par,html).group(2)
        return data
    except:
        return -1
def translate(string):
    data = {'doctype': 'json','type': 'AUTO','i':string}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    result = result['translateResult'][0][0]["tgt"]
    return result
def getweather(province,city):
    tf=0
    data = {'doctype': 'json','type': 'AUTO','i':province}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    province = result['translateResult'][0][0]["tgt"]
    data = {'doctype': 'json','type': 'AUTO','i':city}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    city = result['translateResult'][0][0]["tgt"]
    try:
        wurl="https://tianqi.moji.com/weather/china/"+province+'/'+city
        html = urllib.request.urlopen(wurl).read().decode("utf-8")
        par = '(<meta name="description" content=")(.*?)(">)'
        data = re.search(par, html).group(2)
        data = data.replace(",", "，").replace("。", "，").replace("墨迹天气建议您", "爱搜天气助手建议您")
        return data
    except:
        return -1
import json
import requests
from bs4 import BeautifulSoup
def get_newslist():
    import requests
    try:
        newslist=[]
        url="https://i.news.qq.com/trpc.qqnews_web.pc_base_srv.base_http_proxy/NinjaPageContentSync?pull_urls=news_top_2018"
        data=requests.get(url)
        if data.status_code==200:
            data=json.loads(data.text)
            for i in range(len(data['data'])):
                dict={'title':data['data'][i]['title'],'url':data['data'][i]['url']}
                newslist.append(dict)
            return newslist
    except:
        return -1
def get_newstext(url):
    try:
        html = urllib.request.urlopen(url).read().decode("gbk")
        par = '(<meta name="description" content=")(.*?)(">)'
        try:
            data = re.search(par, html).group(2)
            return data
        except:
            return -1
    except:
        return -1

def printf(text,ts=0.1):
    text=str(text)
    for i in text:
        print(i,end='')
        time.sleep(ts)
def cleardevice():
    import sys
    sys.stdout.write("\033[2J\033[00H")
def pagebrowser(text,title):
    from cefpython3 import cefpython as cef
    import platform
    import sys
    try:
        html = urllib.request.urlopen(text).read().decode("utf-8")
        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        cef.CreateBrowserSync(url=text,window_title=title)
        cef.MessageLoop()
        return 0
    except:
        return -1
def get_pcsystem():
    import platform
    return platform.system()
def find_lib(libname):
    try:
        url='http://127.0.0.1:55820/package/search?name='+libname
        a=json.loads(urlopen(url).read().decode())
        if a['data']['option'][0]['state']=='not_installed':
            return False
        elif a['data']['option'][0]['state']=='installed':
            return True
    except:
        return -1
def download_lib(lib):
    os.system(sys.executable + " -m pip install " + lib + " -i https://pypi.douban.com/simple")