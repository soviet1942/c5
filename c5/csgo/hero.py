import random
from urllib import request
import uuid
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from common import ip_agent_pool


class Run(object):
    
    def get_web_content(self, url):
        proxy_support = request.ProxyHandler(self.getRandomProxy())
        opener = request.build_opener(proxy_support)
        opener.addheaders = [('User-Agent',self.getRandomHeaders()),('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')]
        request.install_opener(opener)
        response = request.urlopen(url, timeout=6)
        html = response.read().decode("utf-8")
        bf = BeautifulSoup(html, 'lxml')
        #摘取属性
        all = bf.find_all(class_='mask')
        for i in all:
            image_name = i.get("alt")
            image_src = i.get("src")
            urlretrieve(url = image_src,filename = 'F:\\CSGO\\dota2_hero\\' + image_name + '.png')#图片下载

    
    #获取随机代理和请求头
    def getRandomHeaders(self):
        return random.choice(ip_agent_pool.UserAgents)
    def getRandomProxy(self):
        return random.choice(ip_agent_pool.proxys)
    
if __name__ == '__main__':
    Run().get_web_content("https://www.c5game.com/dota.html");