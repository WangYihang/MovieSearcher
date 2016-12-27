#!/usr/bin/env python
#encoding:utf-8

import requests
from bs4 import BeautifulSoup
import urllib
import sys
import re

# 解决编码错误问题
reload(sys)  
sys.setdefaultencoding('utf8') 

'''
阳光电影模块
'''

# config-start
modelName = "阳光电影"
url = "http://www.ygdy8.com"
keyword = sys.argv[1]
keywordURLencode = urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk')) # 将查询关键字进行URL编码
searchUrl = "http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&keyword=" + keywordURLencode
# config-end

def getContent(url):
    headers = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control' : 'max-age=0',
        'Cookie' : 'PHPSESSID=075a0c375495ba59fdb2b8d3d3280113',
        'Host' : 's.dydytt.net',
        'Proxy-Connection' : 'keep-alive',
        'Referer' : 'http://www.ygdy8.com/',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }
    response = requests.get(url)
    response.encoding = 'gb2312' # 设置相应体的字符集
    return response.text


def getResultNumber(soup):
    td = soup.find("td",width="50")
    a = td.find("a")['href']
    totalResult = str(a).split("&")[-2]
    return int(totalResult.split("=")[1])

def getPageNumber(resultNumber):
    return int((resultNumber / 10)) + 1

def getResultDic(soup):
    results = []
    tables = soup.findAll("table", border='0', width='100%')[1:]
    for table in tables:
        # 获取结果标题
        temptitle = str(table.find("a"))
        temptitle = temptitle.replace("<font color=\"red\">","")
        temptitle = temptitle.replace("</font>","")
        temp = temptitle.split(">")
        title = temp[1].split("<")[0]
        # 获取结果描述
        tempdescribe = str(table.find("td", colspan="3", height="56"))
        tempdescribe = tempdescribe.replace("<font color=\"red\">","")
        tempdescribe = tempdescribe.replace("</font>","")
        temp = tempdescribe.split(">")
        describe = temp[1].split("<")[0]
        # 获取页面详细地址
        src = url + table.find("a")['href']
        # 参考DOM节点 : td style="WORD-WRAP: break-word" bgcolor="#fdfddf"
        newContent = getContent(src)
        newSoup = BeautifulSoup(newContent, "html.parser")
        newtd = newSoup.find("td", style="WORD-WRAP: break-word", bgcolor="#fdfddf")
        downloadLink = newtd.find("a")['href']
        result = {
            "title":title,
            "describe":describe,
            "downloadLink":downloadLink
        }
        results.append(result)
        print "单条数据获取成功 !"
    return results

# 首先根据第一个页面获取总页面数
content = getContent(searchUrl)
soup = BeautifulSoup(content, "html.parser")
resultNumber = getResultNumber(soup)
pageNumber = getPageNumber(resultNumber)


print "查询结果数 :", resultNumber
print "总页面数量 :", pageNumber

print "正在获取第 1 页的结果" 
results = getResultDic(soup)
print "该页所有结果获取成功 !"

for page in range(1, pageNumber):
    print "正在获取第",(page + 1),"页的结果" 
    searchUrl = "http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&keyword=" + keyword + "&PageNo=" + str(page + 1)
    content = getContent(searchUrl)
    soup = BeautifulSoup(content, "html.parser")
    results += getResultDic(soup)
    print "该页所有结果获取成功 !"

# 格式化显示数据 : 
for result in results:
    file = open(modelName + "-" + keyword + ".txt","a+")
    file.write("---------------------------\n")
    file.write("标题 : " + result['title'] + "\n")
    file.write("描述 : \n\t" + result['describe'] + "\n")
    file.write("下载地址 : \n\t" + result['downloadLink'] + "\n")
    file.write("\n")
    file.close()
