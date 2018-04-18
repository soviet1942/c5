'''
Created on 2017年10月18日

@author: Administrator
'''
import re
import uuid
if __name__ == "__main__":
    key = 'SSG 08（StatTrak™） | 幽灵战士 (崭新出厂)'
    result = re.match(r'([“ ]?\w+[- ]?\w*)', key).group().rstrip()
    print(result)
