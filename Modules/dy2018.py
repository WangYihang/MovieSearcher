#!/usr/bin/env python
#encoding:utf-8

import requests
from bs4 import BeautifulSoup
import urllib
import sys
import re
import MySQLdb
import base64

# 解决编码错误问题
reload(sys)    
sys.setdefaultencoding('utf8')

def getHex(words):
    mywords = words.split("%")[1:]
    result = ""
    for i in mywords:
        result += chr(int(i, 16))
    return result

'''
电影天堂模块
'''

# config-start

# 连接数据库
DBhost = "localhost"
DBport = 3306
DBusername = "root"
DBpassword = "duolaAmeng"
DBname = "bigdata"
DBcharset = "utf8"

# 日志文件名
logFileName = "dy2018-log.txt"
headers = {
        'Host' : 'www.dy2018.com',
        'Cache-Control' : 'max-age=0',
        'Origin' : 'http://www.dy2018.com',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer' : 'http://www.dy2018.com/index.html',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection' : 'close'
}
pageSize = 20
url = "http://www.dy2018.com"
modelName = "电影天堂"
keyword = sys.argv[1]
keywordURLencode = urllib.quote(keyword.decode(sys.stdin.encoding).encode('GBK')) # 将查询关键字进行URL编码
searchUrl = "http://www.dy2018.com/e/search/index.php"
postData = {
    'classid':'0',
    'show':'title,smalltext',
    'tempid':'1',
    'keyboard': getHex(keywordURLencode),
    'Submit':chr(0xC1) + chr(0xA2) + chr(0xBC) + chr(0xB4) + chr(0xCB) + chr(0xD1) + chr(0xCB) + chr(0xF7)
}

# config-end


def saveLog(content):
    global logFileName
    logFile = open(logFileName,"a+")
    logFile.write(content + "\r\n")
    logFile.close()

def getContent(url):
    global headers
    response = requests.get(url, headers=headers)
    response.encoding = 'gb2312' # 设置相应体的字符集
    return response.text

def getResultNumber(soup):
    a = soup.find("a", title="总数")
    if a == None:
        return len(soup.findAll("table", width="100%", border="0", cellspacing="0", cellpadding="0", class_="tbspan", style="margin-top:6px"))
    else:
        return int(a.find("b").string)

def getResponseByPostData(url,postData):
    global headers
    return requests.post(url, data=postData, headers=headers)

def getPageNumber(resultNumber):
    global pageSize
    return int((resultNumber / pageSize)) + 1

def getPageID(url):
    pageID = url.split(".html")[0].split("-")[1]
    return pageID

def getResultDic(soup, keyboard):
    results = []
    tables = soup.findAll("table", width="100%", border="0", cellspacing="0", cellpadding="0", class_="tbspan", style="margin-top:6px")
    for table in tables:
        # 获取结果标题
        title = str(table.find("a")["title"])
        # 获取结果描述
        describe = table.find("td", colspan="2", style="padding-left:3px").string
        # 获取页面详细地址
        src = url + table.find("a")['href']
        # 获取条目时间和点击量
        temp = table.find("font", color="#8F8C89").string
        time = temp.split("\n")[0].split("：")[1][0:-1] # 注意这里是中文冒号
        click = temp.split("\n")[1].split("：")[1] # 注意这里是中文冒号
        # 获取下载地址
        downloadLinks = []
        newContent = getContent(src)
        newSoup = BeautifulSoup(newContent, "html.parser")
        tbodys = newSoup.findAll("tbody")
        # if len(tbodys) == 0:
        #     # 说明这个资源没有下载地址 , 有可能是因为这个资源可以在线播放 (http://www.dy2018.com/i/96661.html)
        #     break;
        for tbody in tbodys:
            a = tbody.find("a")
            if a == None:
                continue
            downloadLinks.append(a['href'])
        result = {
            "title":title,
            "describe":describe,
            'time':time,
            'click':click,
            "downloadLink":downloadLinks
        }
        results.append(result)
        # print "单条数据获取成功 ! "
        # saveLog("单条数据获取成功 ! ")
        print ".",
        # saveLog("单条数据获取成功 ! ")
        # 当一条数据获取成功以后就立即进行数据库的插入和文件的读写
        # 文件读写
        saveResultToFile(unicode(modelName + "-" + keyword + ".txt", "UTF8"), title, describe, time, click, downloadLinks)
        # 数据库插入
        saveResultToDB(conn, title.encode("utf-8"), describe.encode("utf-8"), time.encode("utf-8"), click.encode("utf-8"), result['downloadLink'], keyword)
    return results

# 文件读写
def saveResultToFile(fileName, title, describe, time, clickTimes, downloadLinks):
    file = open(fileName,"a+")
    file.write("---------------------------\n")
    file.write("标题 : " + title + "\n")
    file.write("描述 : \n\t" + describe + "\n")
    file.write("时间 : " + time + "\n")
    file.write("点击量 : " + clickTimes + "\n")
    file.write("下载地址 : " + "\n")
    for downloadlink in downloadLinks:
        file.write("\t" + downloadlink + "\n")
    file.write("\n")
    file.close()
    # print "已将数据成功保存在本地文件(",fileName,")中!"
    # saveLog("已将数据成功保存在本地文件(" + fileName + ")中!")
    # print "."
    # saveLog("已将数据成功保存在本地文件(" + fileName + ")中!")

# 防注入
def antiSQLInject(content):
    # print "正在对数据的安全性进行检测"
    # saveLog("正在对数据的安全性进行检测")
    # 这里先只做简单的替换(但是不能替换为空 ，如果替换为空的话 , 攻击者可以通过双写来绕过过滤)
    tempContent = content.lower()
    SIGN = True # 标记是否检测到了黑名单中的关键字
    words = ['union','select'] # 这里定义黑名单关键字
    for word in words:
        if word in tempContent:
            SIGN = False
            tempContent.replace(word,"_")
    if SIGN:
        # print "检测通过 , 目前没有发现注入的可能"
        # saveLog("检测通过 , 目前没有发现注入的可能")
        return content
    else:
        # print "检测不通过 , 在内容中发现了敏感内容 , 已经将其过滤 !"
        # saveLog("检测不通过 , 在内容中发现了敏感内容 , 已经将其过滤 !")
        return tempContent
    
    
# 数据库插入
def saveResultToDB(conn, title, describe, time, click, downloadLinks, keyword):
    # 对数据进行编码转换
    # 被编码问题折腾地也是醉了 , 直接base64以后再存数据库吧
    # title = base64.b64encode(title)
    # describe = base64.b64encode(describe)
    # time = base64.b64encode(time)
    # click = base64.b64encode(click)
    # downloadLinks = base64.b64encode(str(downloadLinks))
    # keyword = base64.b64encode(keyword)
    # 将即将插入数据库的数据进行转义
    # title = MySQLdb.escape_string(title)
    # describe = MySQLdb.escape_string(describe)
    # time = MySQLdb.escape_string(time)
    # click = MySQLdb.escape_string(click)
    # downloadLinks = MySQLdb.escape_string(downloadLinks) # 由于下载地址可能有很多 , 因此使用了List来储存 , 但是数据库不支持这种数据结构 , 因此需要转换成string
    # keyword = MySQLdb.escape_string(keyword)
    # 将即将插入数据的数据进行过滤 , 防注入
    # title = antiSQLInject(title)
    # describe = antiSQLInject(describe)
    # time = antiSQLInject(time)
    # click = antiSQLInject(click)
    # downloadLinks = antiSQLInject(downloadLinks)
    # keyword = antiSQLInject(keyword)
    downloadLinkResult = ""
    for downlink in downloadLinks:
        downloadLinkResult += downlink + "</br>"

    cur = conn.cursor()
    cur.execute('SET NAMES UTF8')
    # sql = "insert into movies (`movieTitle`, `movieDescribe`,`movieTime`,`movieClickTimes`, `movieDownloadLink`, `movieKey`) values (\"" + title + "\",\"" + describe + "\",\"" + time + "\",\"" + click + "\",\"" + downloadLinks + "\",\"" + keyword + "\");"
    sql = "insert into movies (`movieTitle`, `movieDescribe`,`movieTime`,`movieClickTimes`, `movieDownloadLink`, `movieKey`) values ('%s','%s','%s','%s','%s','%s')" % (title,describe,time,click,downloadLinkResult,keyword) # SQL参数化 , 参数化的好处是python直接就帮我们进行了一次数据类型的转换
    cur.execute(sql)
    conn.commit()
    # print "已将结果成功插入数据库中!"
    # saveLog("已将结果成功插入数据库中!")



print "正在连接数据库...",
saveLog("正在连接数据库...",)
conn = MySQLdb.connect(DBhost,DBusername,DBpassword,DBname,charset=DBcharset)
print "数据库连接成功!"
saveLog("数据库连接成功!")

print "正在获取搜索结果..."
saveLog("正在获取搜索结果...")
response = getResponseByPostData(searchUrl, postData)
soup = BeautifulSoup(response.text.decode("UTF-8"), "html.parser")
print "搜索结果获取成功!"
saveLog("搜索结果获取成功!")
print "正在获取结果数量..."
saveLog("正在获取结果数量...")
resultNumber = getResultNumber(soup)
print "查询结果数 :", resultNumber
saveLog("查询结果数 :" + str(resultNumber))
pageNumber = getPageNumber(resultNumber)
print "总页面数量 :", pageNumber
saveLog("总页面数量 :" + str(pageNumber))
pageID = getPageID(response.url)
print "缓存页面名 :",pageID
saveLog("缓存页面名 :" + str(pageID))

# # 让用户选择需要获取多少页面的数据
# needPageNumber = input("请输入需要获取的数据的页面数量(Max = " + str(pageNumber) + ") : ")

# while True:
#     if needPageNumber > pageNumber:
#         needPageNumber = input("请输入需要获取的数据的页面数量(Max = " + str(pageNumber) + ") : ")
#     else:
#         break

# # 将用户输入的数字字符串转成数字
# try:
#     needPageNumber = int(needPageNumber)
# except:
#     print "输入页码错误 , 已经默认将页码设置为 : ",pageNumber
#     saveLog("输入页码错误 , 已经默认将页码设置为 : " + str(pageNumber))
#     needPageNumber = pageNumber

# 给用户使用的时候为了节省流量 , 需要让用户进行判断
# 但是现在是在服务器上当一个服务跑 , 因此不需要与用户进行交互 ， 直接默认所有数据
needPageNumber = pageNumber
for i in range(needPageNumber):
    if i == 0: # 由于第一页已经获取过了 , 因此可以直接使用缓存
        print "---------------------"
        print "正在获取第 1 页的结果" 
        saveLog("正在获取第 1 页的结果" )
        results = getResultDic(soup, keyword)
        print "\n该页所有结果获取成功 !"
        saveLog("该页所有结果获取成功 !")
    else:
        print "---------------------"
        print "正在获取第",(i + 1),"页的结果"
        saveLog("正在获取第" + str((i + 1)) + "页的结果")
        thisUrl = "http://www.dy2018.com/e/search/result/searchid-" + pageID + "-page-" + str(i) + ".html"
        tempContent = getContent(thisUrl)
        tempSoup = BeautifulSoup(tempContent, "html.parser")
        results += getResultDic(tempSoup, keyword)
        print "\n该页所有结果获取成功 !"
        saveLog("该页所有结果获取成功 !")

print "数据获取完毕 ! "
saveLog("数据获取完毕 ! ")

# 关闭数据的连接
conn.close()
print "数据库连接已关闭!"
saveLog("数据库连接已关闭!")






