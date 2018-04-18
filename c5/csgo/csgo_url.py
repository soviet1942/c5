'''
Created on 2017年10月25日

@author: Administrator
'''
from urllib import request
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import re
import pymysql
import time
import uuid
import random

from commons.mylog import my_log
from commons import ip_agent_pool

url_base = "https://www.c5game.com/csgo/default/result.html?type={}&page={}&exterior=WearCategory{}&sort=price"
url_base_other = "https://www.c5game.com/csgo/default/result.html?type={}&page={}&sort=price"
href_set = set()#用来存放要访问的地址的set集合

def geturls(itemtype):
    proxy_support = request.ProxyHandler(getRandomProxy())
    opener = request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',getRandomHeaders()),('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')]
    request.install_opener(opener)
    #遍历所有exterior
    for exterior in range(0,5):
        page = 1
        while True:
            url = url_base.format(itemtype, page, exterior)
            try: 
                latch = inner_page(url, page)
            except: 
                inner_page(url, page)
            else:
                if(latch == "break"):
                    break
                print("itemtype"+str(itemtype)+"   exterior"+str(exterior)+"   page"+str(page))
                page = page+1
    print("over")

def geturls_other(itemtype):
    proxy_support = request.ProxyHandler(getRandomProxy())
    opener = request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',getRandomHeaders()),('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')]
    request.install_opener(opener)
    #遍历所有exterior
    page = 1
    while True:
        url = url_base_other.format(itemtype, page)
        try: 
            latch = inner_page(url, page)
        except: 
            inner_page(url, page)
        else:
            if(latch == "break"):
                break
            print("itemtype"+str(itemtype)+"   page"+str(page))
            page = page+1
    print("over")   
        
def inner_page(url, page):
    response = request.urlopen(url, timeout=5)
    html = response.read().decode("utf-8")
    bf = BeautifulSoup(html, 'lxml')
    items_result = bf.find(class_='list-item4').find_all(class_='csgo-img-bg')
    if(len(items_result) == 0):
        return "break"
    for hrefs in items_result:
        href = 'https://www.c5game.com'+hrefs.get('href')
        href_set.add(href)


def getRandomHeaders():
    return random.choice(ip_agent_pool.UserAgents)
def getRandomProxy():
    return random.choice(ip_agent_pool.proxys)
    
    
    
if __name__ == "__main__":
    types = ["csgo_type_knife","csgo_type_pistol","csgo_type_rifle","csgo_type_sniperrifle","csgo_type_smg","csgo_type_shotgun","csgo_type_machinegun","type_hands"]
    other_types = ["csgo_type_weaponcase","csgo_tool_sticker","csgo_type_musickit","csgo_type_collectible","csgo_type_spray","csgo_tool_name_tagtag","csgo_type_ticket"]
    for i in range(len(types)):
        geturls(types[i])
    #for i in range(len(other_types)):
    #    geturls_other(other_types[i])
    f = open("txt/csgo_url.txt","w")
    f.write(str(href_set)) 
    