#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# import cookielib
# import urllib2
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver  #导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  #导入Keys

driver = webdriver.Chrome()  #指定使用的浏览器，初始化webdriver
driver.get("http://yuanjian.cnki.net/cjfd/Home/Detail/WYXY201804")  #请求网页地址
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
# url = 'http://www.cnki.com.cn/Article/CJFDTOTAL-WYXY201805005.htm'
# r = requests.get(url,headers=headers) #像目标url地址发送get请求，返回一个response对象
# soup = BeautifulSoup(r.text, 'lxml')
csv_header=['题目','URL']
f = open('paper_urls.csv','w',newline='')
writer = csv.writer(f) 
writer.writerow([csv_header])
			        
soup = BeautifulSoup(driver.page_source, 'lxml')
all_div = soup.find('div',id='divCJFDCatalog').find_all('div',class_='l-box')#获取栏目
for div in all_div:
	column = div.find('div').string.strip() #栏目名
	if column:
		# print('\n',column)
		tab_lefts = div.find_all('div',class_='tab-left')
		titles=[i.find('a') for i in tab_lefts]
		for title in titles:
			title_name=title.string
			url=title['href']
			print('\n',title_name)
			writer.writerow([title_name,url])

			driver.get(url)
			soup = BeautifulSoup(driver.page_source, 'lxml')
			abstract = soup.find('div', style="text-align:left;word-break:break-all")
			print(abstract.get_text())
			# for i in abstract:
			# 	print("________",i)

f.close()
driver.close()
# title = soup.find('h1',{'class':'xx_title'}).string
# abstract = soup.find_all('div', style="text-align:left;word-break:break-all")
# for i in abstract:
# 	print(i.string)
