from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import random
import re
import time
from urllib import request
from urllib.request import urlretrieve
import uuid

from bs4 import BeautifulSoup
import pymysql

from commons import ip_agent_pool
from commons.mylog import my_log


#字典
exterior_list = ['崭新出厂', '略有磨损', '久经沙场', '破损不堪', '战痕累累', '无涂装']
type_filter_arr = ['印花', '音乐盒', '胸章', '涂鸦', '标签', '通行证', '武器箱', '钥匙']
quality_dic = {'text-unique':'无', 'text-normal':'普通', 'text-strange':'StatTrak™', 'text-tournament':'纪念品', 'text-unusual':'★', 'text-genuine':'纯正'}
rarity_dic = {'rarity-ancient_weapon':'无', 'rarity-mythical':'受限', 'rarity-ancient':'隐秘', 'rarity-common':'普通级', 'rarity-rare':'军舰级', 'rarity-uncommon':'工业级', 'rarity-legendary':'保密', 'rarity-contraband':'违禁', 'rarity-immortal':'保密'}
type_dic = {'csgo_type_collectible':'胸章', 'csgo_type_musickit':'音乐盒', 'csgo_type_spray':'涂鸦'}

class TestThreadPoolExecutor(object):
    def __init__(self):
        self.count = 0
        self.err_count = 0#监视错误的次数
        _log = my_log
        f = open("txt/csgo_url.txt",'r')
        self.urls = f.readline().strip("[{}']").split("', '")
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234',db='game',charset='utf8')
        self.cursor = self.conn.cursor() 

    def get_web_content(self, url=None):
        try:
            proxy_support = request.ProxyHandler(self.getRandomProxy())
            opener = request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent',self.getRandomHeaders()),('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')]
            request.install_opener(opener)
            response = request.urlopen(url, timeout=6)
            html = response.read().decode("utf-8")
            bf = BeautifulSoup(html, 'lxml')
            item_attr = bf.find(class_='ft-gray').find_all('span')
            ifcsgo = re.findall(r'class="(.*)"', str(item_attr[0]))[0]
            if(ifcsgo != "icon-csgo"): return#如果种类不是csgo那就跳过吧
            quality = quality_dic.get(re.findall(r'class="(.*)"', str(item_attr[1]))[0])
            rarity = rarity_dic.get(re.findall(r'class="(.*)"', str(item_attr[2]))[0])
            csgotype = item_attr[3].get_text()
            if(type_dic.get(csgotype)!= None):
                csgotype = type_dic.get(csgotype)
            name_url = bf.find(class_='sale-item-info').find(class_="name")
            name_text = name_url.span.get_text().strip()
            item_type = re.match(r'([“ ]?\w+[- ]?\w*)', name_text).group().rstrip()
            if(type_filter_arr.__contains__(csgotype)): item_type = csgotype
            item_exterior = re.findall(r'\(([\u4E00-\u9FA5]*)\)', name_text)
            exterior = "无"
            if(item_exterior.__len__()==1):
                if(exterior_list.__contains__(item_exterior[0])):
                    exterior = item_exterior[0]
            price_ = bf.find(class_='hero')
            price = re.findall(r'￥[ ]?(\d+[.]?\d*)', price_.span.get_text())[0]
            sales_ = bf.find(class_='sale-items-sty1').find('li')
            sales = sales_.span.get_text()
            img_url = bf.find(class_='sale-item-img csgo-img-bg text-center imgs')
            img_src = str(img_url.img.get('src'))
            image_n = re.sub(r'\([\u4E00-\u9FA5]*\)', "", name_text).rstrip()
            image_name = uuid.uuid3(uuid.NAMESPACE_DNS, image_n).__str__()
            self.cursor.execute("INSERT INTO csgo_item (type,item_type,item_name,price,img,exterior,quality,rarity,sales) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"% (csgotype,item_type,name_text,price,image_name,exterior,quality,rarity,sales)) 
            self.conn.commit()
            self.count = self.count + 1
            count_str = str(self.count)
            print(count_str+"=====name:"+name_text+"type:"+csgotype+"item_type:"+item_type+"price:"+price+"exterior:"+exterior+"quality:"+quality+"rarity:"+rarity+"sales:"+sales+"img"+image_name)
            data = {"image_name":image_name,"img_src":img_src}
            #data = {"url":url, "name_text":name_text, "csgotype":csgotype,"item_type":item_type,"price":price,"exterior":exterior,"quality":quality,"rarity":rarity,"sales":sales,"image_name":image_name,"img_src":img_src,"image_name":image_name}
        except:
            print("网络可能出现异常，即将重试，最多3次")
            data = None
            if self.err_count < 3:
                TestThreadPoolExecutor.get_web_content(url)
                err_count = self.err_count + 1
            elif err_count >= 3: 
                err_count = 0
                data = None
                print()("出现错误，url:"+url)
        else:
            err_count = 0
            return data

    def runner(self):
        thread_pool = ThreadPoolExecutor(max_workers=5)
        futures = dict()
        for url in self.urls:
            future = thread_pool.submit(self.get_web_content, url)#造子弹
            futures[future] = url#用url给子弹标上号然后放入子弹箱

        for future in concurrent.futures.as_completed(futures):#取子弹
            try:
                url = futures[future]#得到子弹的标号
                crawl_result = future.result()
                urlretrieve(url = crawl_result['img_src'],filename = 'F:\\CSGO\\csitem\\' + crawl_result["image_name"] + '.png')
                time.sleep(3)
                #数据库的插入
                #self.cursor.execute("INSERT INTO csgo_item (type,item_type,item_name,price,img,exterior,quality,rarity,sales) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                #               % (crawl_result["csgotype"],crawl_result["item_type"],crawl_result["name_text"],crawl_result["price"],crawl_result["image_name"],crawl_result["exterior"],crawl_result["quality"],crawl_result["rarity"],crawl_result["sales"])) 
                #self.conn.commit()
            except:
                print("线程取出出现错误")
                continue
        print('Finished!')
    
    #获取随机代理和请求头
    def getRandomHeaders(self):
        return random.choice(ip_agent_pool.UserAgents)
    def getRandomProxy(self):
        return random.choice(ip_agent_pool.proxys)
    
if __name__ == '__main__':
    TestThreadPoolExecutor().runner()