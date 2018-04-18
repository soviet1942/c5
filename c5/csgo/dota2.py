from concurrent.futures import ThreadPoolExecutor
import random
import re
from urllib import request
import uuid
from bs4 import BeautifulSoup
import pymysql
from urllib.request import urlretrieve
from common import ip_agent_pool


class TestThreadPoolExecutor(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234',db='game',charset='utf8')
        self.cursor = self.conn.cursor() 
    
    def get_web_content(self, url, index):
        try:
            #基础部分
            proxy_support = request.ProxyHandler(self.getRandomProxy())
            opener = request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent',self.getRandomHeaders()),('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')]
            request.install_opener(opener)
            response = request.urlopen(url, timeout=6)
            html = response.read().decode("utf-8")
            bf = BeautifulSoup(html, 'lxml')
            #摘取属性
            if(bf.find_all(class_='ft-gray mt-5')[1].find("a") != None):
                hero = bf.find_all(class_='ft-gray mt-5')[1].find("a").get_text().strip()#英雄名称
            else: hero = ""
            item_attr = bf.find(class_='ft-gray mt-5').find_all('span')
            name = bf.find(class_='sale-item-info').find(class_="name").span.get_text().strip()#饰品名称
            quality = item_attr[1].get_text().strip();#品质
            rarity = item_attr[2].get_text().strip();#稀有度
            item_type = item_attr[3].get_text().strip();#种类
            price = re.findall(r'￥[ ]?(\d+[.]?\d*)', bf.find(class_='hero').span.get_text())[0]#价格
            sales = bf.find(class_='sale-items-sty1').find('li').span.get_text()#销量
            image_name = uuid.uuid3(uuid.NAMESPACE_DNS, name).__str__()#图片uuid名称
            image_src = str(bf.find(class_='sale-item-img csgo-img-bg text-center imgs').img.get('src'))#图片下载地址
            urlretrieve(url = image_src,filename = 'F:\\CSGO\\dota2_item\\' + image_name + '.png')#图片下载
            print(str(index)+"=====name:"+name+" type"+item_type+" quality"+quality+" rarity"+rarity+" hero"+hero+" price"+price+" img"+image_name+" sales"+sales)
            try:
                #数据库插入
                self.cursor.execute("INSERT INTO dota2_item (item_name,type,quality,rarity,hero,price,img,sales) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"% (name,item_type,quality,rarity,hero,price,image_name,sales)) 
                self.conn.commit()
            except:
                self.conn.rollback()
                print("数据库插入错误，回滚操作")
        except:
            print("网络异常:"+url);

    def runner(self):
        thread_pool = ThreadPoolExecutor(max_workers=5)
        for index in range(22311,22312):
            url = "https://www.c5game.com/dota/"+str(index)+"-S.html"
            try:
                thread_pool.submit(self.get_web_content, url, index)#提交方法到线程池中
            except Exception:
                print("线程出现错误")
    
    #获取随机代理和请求头
    def getRandomHeaders(self):
        return random.choice(ip_agent_pool.UserAgents)
    def getRandomProxy(self):
        return random.choice(ip_agent_pool.proxys)
    
if __name__ == '__main__':
    TestThreadPoolExecutor().runner()