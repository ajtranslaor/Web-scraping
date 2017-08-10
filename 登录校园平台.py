#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 00:07:24 2017

@author: aj
"""

from selenium import webdriver
driver = webdriver.Chrome('/Users/aj/Desktop/RStudio.app/chromedriver')
driver.get("http://www.yzgzx.com")
driver.find_element_by_xpath('/html/body/div[2]/div/a').click()
driver.title
driver.switch_to_window(driver.window_handles[1])
driver.find_element_by_css_selector('#username').send_keys("20090804")
driver.find_element_by_css_selector('#password').send_keys("196131")                            
driver.find_element_by_xpath('//*[@id="casLoginForm"]/div[2]/button').click()
js = " window.open('http://www.juti.cn/')" 
driver.execute_script(js)
js = " window.open('http://jyj.yangzhou.gov.cn')" 
driver.execute_script(js)
driver.quit()
driver.close()