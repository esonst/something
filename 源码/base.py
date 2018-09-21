import re
from bs4 import BeautifulSoup
import requests

def get_cookies_pic(url):
    try:
        cook=requests.get(url,timeout=5)
    except:
        print("连接超时")
    jar=requests.cookies.RequestsCookieJar()
    jar.set('ASP.NET_SessionId',cook.cookies['ASP.NET_SessionId'],domain='202.4.152.190')
    with open('logcode.gif', 'wb') as f:
        f.write(cook.content)
    return jar

def login_post(flag,url,jar):
    if flag:
        try:
            with open("pass.txt","r") as f:
                info=f.read()
            if(info==''):
                print("本地无保存密码")
                raise Exception('无保存密码')
            stuid=info[:10]
            password=info[10:]
            print("stuid="+stuid)
            print("password="+password)
        except:
            stuid=input("student_id=")
            password=input("password=")
    else:
        stuid=input("id=")
        password=input("password=")
    checkcode=input("验证码=")
    data={"__VIEWSTATE":"/wEPDwUENTM4MWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFEl9jdGwwOkltYWdlQnV0dG9uMQ0NODyO1wx8Du/Dppbl8bfJw0UTfwwIEHKsvYbP9Nqt",
      "__EVENTVALIDATION":" /wEWBQKD7ogKAs351pYFAoWvzpoEAo/yj6QJAvejy/sN4orIb7P+pLUuRnP+SEJjmDK905Y49c5EptEPq4AmsvQ=",
      "_ctl0:txtusername":stuid,
      "_ctl0:txtpassword":password,
      "_ctl0:txtyzm":checkcode,
      "_ctl0:ImageButton1.x":"56",
      "_ctl0:ImageButton1.y":"12"
     }
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        req=requests.post(url,data=data,cookies=jar,headers=headers,timeout=5)
    except:
        print("连接超时")
    return req,stuid,password,checkcode


def get_signcode(signurl,jar):
    cook=requests.get(signurl,cookies=jar)
    with open('signcode.gif', 'wb') as f:
        f.write(cook.content)
def signclass(signurl,stuid,jar):
    get_signcode(signurl,jar)
    n=int(input("要抢课的序号:"))
    signcode=input("验证码=")
    data={"__EVENTTARGET":"dgData00$_ctl"+str(n+2)+"$Linkbutton3",
         "__EVENTARGUMENT":"",
         "__VIEWSTATE":"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",
         "__EVENTVALIDATION":"/wEWEgLTm7h4Ari7+5ULAvbGx/QJArGP58MLArGP+54EApL76rYEAv+20uwCAv+2xjECgrf2swoCgrfi+AcCgLfaqgICgLe+7w8C/7a+iQoC/7bazgcC/bbC8AMC/bbWtQECgLemxwsCgLeyjAmSD6wCS8bOOGWilZlBpeeiW0RUr8vF8v3I98Q/CfsMfQ==",
         "txtyzm":signcode}
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        req=requests.post("http://202.4.152.190:8080/pyxx/txhdgl/hdlist.aspx?xh="+stuid,data=data,cookies=jar,headers=headers,timeout=5)
    except:
        print("连接超时")
    print(re.findall("alert.*\)",req.text)[0])

def printf(alist):
    n=0
    for i in range(len(alist)):
        if(alist[i][6]<alist[i][7]):
            print(str(i)+":  ")
            print(alist[i])
            n+=1
    return n