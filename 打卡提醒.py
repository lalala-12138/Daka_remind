# -*- coding: utf8 -*-
import json
import time
import urllib.parse
import requests
import warnings

warnings.filterwarnings("ignore")

def login():
    #此处填管理员的账号密码
    username = ""
    password = ""
    loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
    loginHeader ={
        "Host": "student.wozaixiaoyuan.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us,en",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "Referer": "https://servicewechat.com/wxce6d08f781975d91/147/page-frame.html",
        "Content-Length": "360"
    }
    data = "{}"
    session = requests.session()
    url = loginUrl + "?username=" + username + "&password=" + password

    respt = session.post(url, data=data, headers=loginHeader)
    print(respt.text)
    res = json.loads(respt.text)
    if res["code"] == 0:
        print("Login success.")
        jwsession = respt.headers['JWSESSION']

    else:
        print(res)
        jwsession = 'Login failed.'
    print(jwsession)
    burl=urllib.parse.quote(jwsession)
    dataa="contentType=txt&title={}&content={}&updateTime={}".format(mine,burl,str(time.time))
    requests.post(url="https://api.notelive.cn/server/replaceOrInsertOne", data=dataa, headers= {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    return jwsession

def warn():

    warnUrl = "https://student.wozaixiaoyuan.com/heat/getHeatUsers.json"
    dateToday = time.strftime("%Y" + "%m" + "%d")
    timestr = time.strftime("%H")
    #本地测试
    # if 0 <= int(timestr) < 12:
    # 云端运行
    if 8 <= int(timestr)+8 < 12 or 24 <= int(timestr)+8 < 32:

        seq = "1"
        name="晨检"
    else:
        seq = "2"
        name="午检"


    data = {
        "seq": str(seq),
        "date": dateToday,
        "type": "0"
    }

    resJson = requests.post(url=warnUrl, headers=headers, data=data, verify=False).json()
    # print(resJson)
    try:
        count = 0
        list = []
        nameList=[]
        # print("未打卡成员信息如下：")
        for i in resJson["data"]:
            #此处电话信息来源于我在校园，和企业微信不同可通过.replace()修改
            # print(i["name"] + i["phone"])
            list.append(i["phone"])
            nameList.append(i['name'])
            count = count + 1
        text=str(name)+"未打卡人数：" + str(count)
    except:
        text=resJson['message']
        print(text)
    else:
        print(text)
        if count !=0:
            recentBody = {
                "msgtype": "text",
                "text": {
                    "content": text+"\n💫温馨提示: 请尽快打卡",
                    "mentioned_mobile_list": list

                }
            }
            #此处填企业微信机器人api
            recentUrl = ""
            requests.post(url=recentUrl, json=recentBody, headers={'Content-Type': 'application/json; charset=UTF-8'}, verify=False)
        else:
            print("全部打卡")

# if __name__ == "__main__":
def handler(event, context):
    global headers
    global dayNotice
    global mine
    #此处见readme
    mine=""
    cityUrl = "https://api.notelive.cn/render/{}".format(mine)
    cityRes = requests.get(cityUrl)
    jwsession = cityRes.text
    url = "https://student.wozaixiaoyuan.com/heat/get15Days.json"
    headers = {
        "POST": "/heat/getHeatUsers.json HTTP/1.1",
        "Host": "student.wozaixiaoyuan.com",
        "JWSESSION": jwsession,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "Referer": "https://servicewechat.com/wxce6d08f781975d91/186/page-frame.html",
    }
    dayNotice = requests.get(url=url, headers=headers, json={}, verify=False).json()
    if dayNotice['code']==0:
        print("##令牌未过期")
    else:
        print("##令牌已过期，进入登录流程")
        login()
        cityUrl = "https://api.notelive.cn/render/{}".format(mine)
        cityRes = requests.get(cityUrl)
        jwsession = cityRes.text
        headers = {
            "POST": "/heat/getHeatUsers.json HTTP/1.1",
            "Host": "student.wozaixiaoyuan.com",
            "JWSESSION": jwsession,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxce6d08f781975d91/186/page-frame.html",
        }
        dayNotice = requests.get(url=url, headers=headers, json={}, verify=False).json()
    warn()
    return "运行成功"





