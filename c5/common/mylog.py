'''
Created on 2017年10月25日

@author: Administrator
'''
import logging
import getpass
import sys

class my_log(object):
    def __init__(self):
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user) 
        self.logger.setLevel(logging.DEBUG)
        
        #日志文件名
        self.logFile = sys.argv[0][0:-3] + '.log'
        self.formatter = logging.Formatter('%(asctime)s  %(message)s\r\n')
        
        #日志显示到屏幕上并输出到日志文件内
        self.logHand = logging.FileHandler(self.logFile, encoding="utf-8")
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.INFO)
        
        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.INFO)
        
        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)
        
    
        