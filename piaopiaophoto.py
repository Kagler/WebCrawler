import requests
import re
from bs4 import BeautifulSoup
import os
import socket
import time

socket.setdefaulttimeout(30)

def getImgNext(start_url, allimg_urllist):
    html=requests.get(start_url,timeout=30)
    demo=html.text
    soup=BeautifulSoup(demo,'html.parser')
    a=soup.find_all('img')
    for i in a:
        try:
            src=i.attrs['src']
            src1=src.replace("jpg","html")
            src2=src1.replace("Photo","siwameitui")
            allimg_urllist.append(src2)
        except:
            continue

def getImgurl(eachImg_url,eachImg_urllist):
    html=requests.get(eachImg_urllist,timeout=30)
    demo=html.text
    soup=BeautifulSoup(demo,'html.parser')
    a=soup.find_all('img')
    for i in a:
        try:
            src=i.attrs['src']
            eachImg_url.append(re.findall(r"http.*?\.jpg",src)[0])
        except:
            continue

def getImgname(eachImg_url):
    html=requests.get(eachImg_url,timeout=30)
    html.encoding=html.apparent_encoding
    demo=html.text
    soup=BeautifulSoup(demo,'html.parser')
    a=soup.title.string
    return a

def downloadPic(each_url,root,Imgsname):
    path=root+Imgsname+"//"+each_url.split('/')[-1]
    root1=root+Imgsname+"//"
    try:
        if not os.path.exists(root1):
            os.mkdir(root1)
        if not os.path.exists(path):
            r=requests.get(each_url)
            with open(path,'wb') as f:
                f.write(r.content)
                print("文件保存成功")
        else:
            print("文件已存在")
    except:
        print("抓取失败")
        
def main():
    start_url="http://www.ppmsg.net/siwameitui/"
    root="飘飘美女网图片//"
    allimg_urllist=[]
    eachImg_url=[]
    i=0
    getImgNext(start_url,allimg_urllist)
    for eachImg_urllist in allimg_urllist:
        getImgurl(eachImg_url,eachImg_urllist)
        Imgsname=getImgname(eachImg_urllist)
        for each_url in eachImg_url:
            print("正在下载漂漂美女网站<<"+Imgsname+">>第"+str(i+1)+"张图片来自："+str(each_url))
            if not os.path.exists(root):
                os.mkdir(root)
            downloadPic(each_url,root,Imgsname)
            i=i+1
        time.sleep(5)
        i=0
        del eachImg_url[:]
    print("下载完成！")
main()
