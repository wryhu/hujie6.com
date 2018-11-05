# coding=utf-8
import urllib, urllib2
import re
import time, random
import hashlib
import sys

# python2默认ascii编码，已经过时了
reload(sys)
sys.setdefaultencoding('utf-8')


class Translate:
    def __init__(self, key, lan1="AUTO", lan2="AUTO"):
        self.key = key
        self.lan1 = lan1
        self.lan2 = lan2
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    def getSalt(self):
        salt = int(time.time()*1000) + random.randint(0,10)
        return salt

    def getMD5(self, v):
        md5 = hashlib.md5()
        md5.update(v)
        sign = md5.hexdigest()
        return sign

    def getSign(self, key, salt):
        # key = key.encode()
        sign = 'fanyideskweb' + key + str(salt) + "ebSeFb%=XZ%T[KZ)c(sy!"
        sign = self.getMD5(sign)
        return sign

    def youdao(self):
        self.salt = self.getSalt()
        data = {
            "i": self.key,
            "from": self.lan1,
            "to": self.lan2,
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": str(self.salt),
            "sign": self.getSign(self.key, self.salt),
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action":"FY_BY_REALTIME",
            "typoResult": "false"
        }
        data = urllib.urlencode(data)
        headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Connection": "keep-alive",
                    "Content-Length": len(data),
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": "OUTFOX_SEARCH_USER_ID=-391420597@10.168.1.8; JSESSIONID=aaacVRc_vIiemgTpW1krw; OUTFOX_SEARCH_USER_ID_NCOO=1920042841.903593; fanyi-ad-id=46607; fanyi-ad-closed=1; ___rl__test__cookies=1530264003877",
                    "Host": "fanyi.youdao.com",
                    "Origin": "http://fanyi.youdao.com",
                    "Referer": "http://fanyi.youdao.com/",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
        }
        req = urllib2.Request(url=self.url, data=data, headers=headers)
        rsp = urllib2.urlopen(req)
        html = rsp.read()
        html = re.findall(r'"tgt":"([^"]+)"', html)
        return html[0]





