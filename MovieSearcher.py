#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import os
import time
import sys
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

# config-start
# 日志文件名
logFileName = "manager-log.txt"
# 数据库配置
DBhost = "localhost"
DBport = 3306
DBusername = "ubuntu"
DBpassword = "admin123"
DBname = "bigdata"
DBcharset = "utf8"
interval = 60 #  设置间隔多少秒进行一次数据库查询和数据获取 , 单位是秒

# config-end

def saveLog(content):
    global logFileName
    logFile = open(logFileName,"a+")
    logFile.write(content + "\r\n")
    logFile.close()

def task():
    saveLog("正在连接数据库...")
    print "正在连接数据库..."
    db = MySQLdb.connect(DBhost,DBusername,DBpassword,DBname,charset=DBcharset)
    saveLog("数据库连接成功 !")
    print "数据库连接成功 !"
    cursor = db.cursor()
    sql = "SELECT * FROM queue WHERE `status` = \"0\""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        saveLog("总共有" + str(len(results)) + "条关键字等待查询...")
        print "总共有",len(results),"条关键字等待查询..."
        counter = 0
        for row in results:
            print "******************************"
            counter += 1
            keyword = row[1]
            saveLog("正在使用第" + str(counter) + "个关键字 : " + str(keyword) + "进行查询...")
            print "正在使用第", counter ,"个关键字 : ",keyword,"进行查询..."
            
            command = "(/usr/bin/env python dy2018.py " + keyword + ")"
            os.system(command)
            # print command
            # subprocess.call(command) # 这里使用 subprocess 库进行子进程的调用
            # 调用别的python文件
            
            # 这里命令执行完成之后 , 要修改标志位
            sql = "UPDATE queue SET `status` = '1' where `keyword` = \"" + keyword + "\";"
            cursor.execute(sql)
            db.commit()
    except Exception as e:
        print e
        saveLog("sql语句执行失败 ! ")
        print "sql语句执行失败 ! "
    db.close()
    saveLog("数据库关闭成功 !")
    print "数据库关闭成功 !"

def timer(n):  
    while True:
        saveLog("--------------------------")
        print "--------------------------"
        saveLog(time.strftime('%Y-%m-%d %X',time.localtime()))
        print time.strftime('%Y-%m-%d %X',time.localtime())
        task()
        time.sleep(n)  
  
if __name__ == '__main__':
    timer(interval)
