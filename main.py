# -*- coding:utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import re
import pymysql


#功能：
#1.爬取笑话
#2.判断笑话是不是在数据库中
#3.不在就存入数据库中
#4.发送到邮箱
#
#
#
#
#
#
#解析URL
def req(url):
	req = request.Request(url)
	req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36")
	resp = request.urlopen(req)
	soup = BeautifulSoup(resp,'html.parser')
	return soup

#输出笑话内容
def qiushis(soup):
	qiushis = soup.findAll("div",{"class":"content"})
	return qiushis

#生成下一页连接
def nextlink(soup):
	nextpage = soup.find('span',{'class':'next'}).parent
	nextlink = "http://www.qiushibaike.com" + nextpage.get('href')
	return nextlink

#检查相同
def findlink(neirong):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='test1',
                             charset='utf8mb4')

#储存笑话
def saveqiushis(qiushis):
	connection = pymysql.connect(host='localhost',
                             user='root',
                             password='673600740',
                             db='test1',
                             charset='utf8mb4')
	try:
		with connection.cursor() as cursor:
			for qiushi in qiushis:
				print(qiushi.span.get_text(),'\n')
				sql = "insert into `qiushibaike`(`neirong`) values(%s)"
				cursor.execute(sql,(qiushi.span.get_text()))
			connection.commit()
	finally:
		connection.close();



#输入初始URL
url = 'http://www.qiushibaike.com/text/'

#解析连接
soup = req(url) 

#保存笑话
qiushis = qiushis(soup)
saveqiushis(qiushis)
