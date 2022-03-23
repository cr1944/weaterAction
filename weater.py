
#!/usr/bin/python3
#coding=utf-8

import requests, json
import os

SCKEY=os.environ.get('SCKEY') ##Server酱推送KEY
SKey=os.environ.get('SKEY') #CoolPush酷推KEY
def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()  #返回的数据
    english = bee['content']
    zh_CN = bee['note']
    img = bee['picture2']
    str = f"""
# 每日一句

> * {english}
> * {zh_CN}

![img]({img})
"""
    return str

def ServerPush(info): #Server酱推送
    api = "https://sctapi.ftqq.com/{}.send".format(SCKEY)
    title = u"天气推送"
    content = info.replace('\n','\n\n')
    data = {
        "title": title,
        "desp": content
    }
    print(content)
    requests.post(api, data=data)
def CoolPush(info): #CoolPush酷推
    # cpurl = 'https://push.xuthus.cc/group/'+spkey   #推送到QQ群
    # cpurl = 'https://push.xuthus.cc/send/' + SKey  # 推送到个人QQ
    api='https://push.xuthus.cc/send/{}'.format(SKey)
    print(api)
    print(info)
    requests.post(api, info.encode('utf-8'))
def main():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'             #API地址，必须配合城市代码使用
        city_code = '101020600'   #进入https://where.heweather.com/index.html查询你的城市代码
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()         #将数据以json形式返回，这个d就是返回的json数据
        if(d['status'] == 200):     #当返回状态码为200，输出天气状况
            parent = d["cityInfo"]["parent"] #省
            city = d["cityInfo"]["city"] #市
            update_time = d["time"] #更新时间
            forecast = d["data"]["forecast"]
            shidu = d["data"]["shidu"] #湿度
            pm25 = str(d["data"]["pm25"]) #PM2.5
            pm10 = str(d["data"]["pm10"]) #PM10
            quality = d["data"]["quality"] #天气质量

            ganmao = d["data"]["ganmao"] #感冒指数
            tips = d["data"]["forecast"][0]["notice"] #温馨提示
            # 天气提示内容
            tdwt = f"""
# 今日份天气

> {tips}

**城市**： {parent} {city}
**温度**： {wendu}℃
**湿度**： {shidu}
**PM2.5**： {pm25}
**PM10**： {pm10}
**感冒指数**： {ganmao}
**更新时间**： {update_time}
# 一周天气
"""

            tdwt += f"| 今天 |  明天 | {forecast[2]['date']} |{forecast[3]['date']} |{forecast[4]['date']} |{forecast[5]['date']} |{forecast[6]['date']} |\n" \
            "| :------------: |:---------------:| :-----:| :-----:| :-----:| :-----:| :-----:|\n"
            tdwt += f"| {forecast[0]['high']} | {forecast[1]['high']} | {forecast[2]['high']} | {forecast[3]['high']} | {forecast[4]['high']} | {forecast[5]['high']} | {forecast[6]['high']} |\n"
            tdwt += f"| {forecast[0]['low']} | {forecast[1]['low']} | {forecast[2]['low']} | {forecast[3]['low']} | {forecast[4]['low']} | {forecast[5]['low']} | {forecast[6]['low']} |\n"
            tdwt += f"| {forecast[0]['type']} | {forecast[1]['type']} | {forecast[2]['type']} | {forecast[3]['type']} | {forecast[4]['type']} | {forecast[5]['type']} | {forecast[6]['type']} |\n"
            tdwt += f"| {forecast[0]['fx']} | {forecast[1]['fx']} | {forecast[2]['fx']} | {forecast[3]['fx']} | {forecast[4]['fx']} | {forecast[5]['fx']} | {forecast[6]['fx']} |\n"
            tdwt += f"| {forecast[0]['fl']} | {forecast[1]['fl']} | {forecast[2]['fl']} | {forecast[3]['fl']} | {forecast[4]['fl']} | {forecast[5]['fl']} | {forecast[6]['fl']} |\n"
            ServerPush(tdwt +  get_iciba_everyday())
            # CoolPush(tdwt)
    except Exception:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
        print(error)
        print(Exception)

if __name__ == '__main__':
    main()
    
