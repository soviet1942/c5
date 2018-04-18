'''
Created on 2017年10月20日

@author: Administrator
'''
import re
from bs4 import BeautifulSoup  
from urllib import request
import time
import requests
import array

def find(i):
    target_url = 'http://www.xicidaili.com/nn/{}'.format(i)
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    req = requests.get(url = target_url, headers = headers)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html, 'lxml')
    fast = bf.findAll(class_='bar_inner fast')
    s = set()
    for j in range(0,len(fast)):
        ip = fast[j].parent.parent.parent.find("td").nextSibling.nextSibling.get_text()
        port = fast[j].parent.parent.parent.find("td").nextSibling.nextSibling.nextSibling.nextSibling.get_text()
        #element = {'http':ip+":"+port}
        ip_port = ip+":"+port
        s.add(ip_port)
    result = []
    for k in s:
        string = {'http':k}
        result.append(string)
    print(str(result).strip("[]"))

if __name__ == "__main__":
    find(18)

