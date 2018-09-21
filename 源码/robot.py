
# coding: utf-8

# In[1]:


import re
from bs4 import BeautifulSoup
import requests
from base import *
import time
import getpass
import ctypes
import sys
import shutil


# In[2]:


print("robots V1.0\n")
print("Hello, so happy you can use my robots for signing up the class you want.")
print("if you have any question of any suggest, please feel free to send email to \n\neson.xin@gmail.com\n")
print("My latest version is on the github for \n\nhttps://github.com/esonst/something.git\n")
print("Then, let's begin.\n\n\n\n")


# In[30]:


url="http://202.4.152.190:8080/pyxx/login.aspx"
checkurl=r"http://202.4.152.190:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"
signurl="http://202.4.152.190:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"


# In[34]:


def save(filename,checkcode):
    try:
        shutil.move(filename,".\\dataset\\"+checkcode+".gif")
    except:
        print("请在本目录创建一个名为'dataset'的文件夹")
        raise


# In[35]:


def login(checkurl,url):
    flag=input("自动登陆？ (是/否) y/n: ")=='y'
    while(True):
        jar=get_cookies_pic(checkurl)
        req,stuid,password,checkcode=login_post(flag,url,jar)
        if req.url=='http://202.4.152.190:8080/pyxx/Default.aspx':
            with open("pass.txt","w") as f:
                f.write(stuid+password)
            print("Log in Successful!")
            save("logcode.gif",checkcode)
            return stuid,jar
        else:
            print(re.findall("alert.*\)",req.text)[0])


# In[37]:


stuid,jar=login(checkurl,url)


# In[38]:


def get_info(stuid,jar):
    try:
        ans=requests.get("http://202.4.152.190:8080/pyxx/txhdgl/hdlist.aspx?xh="+stuid,cookies=jar,timeout=5)
    except:
        print("连接超时")
    soup=BeautifulSoup(ans.text,"html.parser")
    target=soup.findAll("table")[-1]
    classnum=len(target.findAll("tr"))-1  # 报告数量
    alist=[[]]*classnum
    for n in range(classnum):
        for info in target.findAll("tr")[n+1].findAll("td")[:11]:
            alist[n]=alist[n]+[info.text]
    return alist
alist=get_info(stuid,jar)


# In[39]:


def choose(n,signurl,stuid,jar):
    while(True):
        signclass(signurl,stuid,jar)
        if not input("请选择报告前的序号:(是/否) y/n ")=='y':
            return


# In[41]:


while(True):
    bar_length=3
    n=0
    for percent in range(0, 3):
        hashes = '#' * int(percent/3.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\r当前可选课数："+str(n)+"\truning: %s"%(hashes + spaces))
        sys.stdout.flush()
        time.sleep(2)
        if(len(alist)>0):
            n=print(alist)
            if(n>0):
                ctypes.windll.user32.MessageBoxA(0,u"有报告了！".encode('gb2312'),u' 信息'.encode('gb2312'),0)
                signcode=choose(len(alist),signurl,stuid,jar)
                save("signcode.gif",signcode)


# In[29]:




