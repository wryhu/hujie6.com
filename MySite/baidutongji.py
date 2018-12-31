# -*- coding:utf-8 -*-
import json
import datetime
import requests


class BaiduTongJi(object):
    def __init__(self, siteId, username, password, token):
        self.siteId = siteId
        self.username = username
        self.password = password
        self.token = token
        self.today = datetime.date.today()

    def getresult(self, method, start_date, end_date, metrics):
        base_url = "https://api.baidu.com/json/tongji/v1/ReportService/getData"
        body = {"header": {"account_type": 1, "password": self.password, "token": self.token,
                           "username": self.username},
                "body": {"siteId": self.siteId, "method": method, "start_date": start_date,
                         "end_date": end_date, "metrics": metrics}}
        response = requests.post(base_url, json.dumps(body))
        the_page = response.text
        return the_page

    def getPvUvAvgTime(self):  # 获取PV、UV、AvgTime
        start_date = str(self.today - datetime.timedelta(days=7)).replace("-", "")
        end_date = str(self.today).replace("-", "")
        result = self.getresult("overview/getTimeTrendRpt", start_date, end_date,
                                "pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time")
        result = json.loads(result)["body"]["data"][0]["result"]["items"]
        data = result[0]
        daterange = [str(x[0])[5:] for x in data]
        pv_count = [x[0] if x[0] != '--' else 0 for x in result[1]]
        visitor_count = [x[1] if x[1] != '--'  else 0 for x in result[1]]
        ip_count = [x[2] if x[2] != '--' else 0 for x in result[1]]
        return daterange, pv_count, visitor_count, ip_count

    def getDiYu(self):
        start_date = "20181101"
        end_date = str(self.today).replace("-", "")
        result = self.getresult("visit/district/a",  start_date, end_date,
                                "visitor_count")
        base = json.loads(result)["body"]["data"][0]["result"]["items"]
        source = [item[0] for item in base[0]]
        count = 0
        for i in source:
            i['value'] = base[1][count][0]
            count += 1
        return source, base[1][0][0]

    def getLatest(self):
        start_date = str(self.today).replace("-", "")
        end_date = str(self.today + datetime.timedelta(days=1)).replace("-", "")
        result = self.getresult("trend/latest/a",  start_date, end_date,
                                "start_time,area,access_page,ip,visit_time,visit_pages")
        base = json.loads(result)["body"]["data"][0]["result"]["items"][1]
        a = [i for i in base if i[1] != '鹤壁']
        for i in a:
            try:
                i[4] = str(int(i[4]) // 60) + "分" + str(int(i[4]) % 60) + "秒"
            except:
                pass
        return a