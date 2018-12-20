# -*-coding:utf8-*-
import json, requests, time, sys

reload(sys)
sys.setdefaultencoding('utf-8')


def tianqi_api(ip):
    url = "https://www.tianqiapi.com/api/?version=v1&ip=" + ip
    res = requests.get(url).text
    html = json.loads(res.decode('unicode_escape'))
    data = html['data'][0]
    data2 = html['data'][1]
    result = html['city'] + ": " + data['date'] + " " + data['week'] + "(今天)" + "<br>" + "最高温度:" + data[
        'tem1'] + " 最低温度:" + data['tem2'] + "<br>" + data['wea'] + " " + data['win'][0] + \
             " " + data['win_speed'] + "<br>空气指数:" + data['air_level'] + " 空气质量:" + data['air_tips'] + "<br>"
    for item in data['index']:
        result += item.values()[0]
    result += "<br><br>" + html['city'] + ": " + data2['date'] + " " + data2['week'] + "(明天)" + "<br>" + "最高温度:" + data2[
        'tem1'] + " 最低温度:" + data2['tem2'] + "<br>" + data2['wea'] + " " + data2['win'][0] + \
              " " + data2['win_speed'] + "<br>"
    for item in data2['index']:
        result += item.values()[0]
    return result
