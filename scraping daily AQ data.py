# -*- coding: utf-8 -*-
"""
Scraping China's city-level daily air quality data
"""
import pandas
import numpy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("http://datacenter.mep.gov.cn/index!MenuAction.action?name=402880fb24e695b60124e6973db30011")
import time
time.sleep(0.1)
driver.find_element_by_link_text("大气").click()
time.sleep(1)
driver.find_element_by_link_text("全国城市空气质量日报").click()
driver.switch_to_frame("iframepage")
V_date=driver.find_element_by_name("V_DATE")  
V_date.send_keys("2017-01-01")
V_date.send_keys(Keys.ESCAPE) 
E_date=driver.find_element_by_name("E_DATE")
E_date.send_keys("2017-08-10")
E_date.send_keys(Keys.ESCAPE) 
driver.find_element_by_css_selector('#toolbarhtml > table > tbody > tr:nth-child(1) > td:nth-child(5) > input').send_keys(Keys.ENTER) 

#从这里循环
for i in range(207):
    if i == 0:
        html_source = driver.page_source
        data = pandas.read_html(html_source)[3]
        driver.find_element_by_link_text("下一页").click()
    else:
        html_source = driver.page_source
        data=data.append(pandas.read_html(html_source)[1])
        driver.find_element_by_link_text("下一页").click()

data=data.drop_duplicates()           #去除重复的行
data.drop(data[[1]], axis=1, inplace=True)   #删除ID列
data.columns=list(numpy.array(data.loc[[0]]))  #更改列名
data.drop(0, axis=0, inplace=True)   #删除第一行
data.drop('序号',axis=1, inplace=True)  #删除序号列
data.to_csv('/Users/aj/Desktop/AQ.csv', encoding='gbk')
data.to_pickle('/Users/aj/Desktop/AQ.pkl')   #将数据存为pickle格式
df = pandas.read_pickle('/Users/aj/Desktop/AQ.pkl')  #读取pickle数据
df=pandas.read_table('/Users/aj/Desktop/中国城市空气质量日报/Untitled.txt',header=None,encoding='UTF-8',delim_whitespace=False)
df = pandas.read_csv('/Users/aj/Desktop/中国城市空气质量日报/Untitled.csv', header = None,low_memory=False)
data[['AQI指数','CITYCODE']] = data[['AQI指数','CITYCODE']].apply(pandas.to_numeric)
df[['AQI指数','CITYCODE']] = df[['AQI指数','CITYCODE']].apply(pandas.to_numeric)
final_data=data.append(df)
final_data.to_pickle('/Users/aj/Desktop/AQ_final.pkl')   #将最终数据存为pickle格式
driver.close()
driver.quit()