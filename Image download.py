#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:06:34 2017

@author: aj
"""

import os
os.getcwd()
os.chdir("/Users/aj/Desktop/img")
from bs4 import BeautifulSoup
import urllib
import shutil
import requests
import sys
import time

def make_soup(url):
    html = urllib.request.urlopen(url).read()
    return BeautifulSoup(html, 'html.parser')

def get_images(url):
    soup = make_soup(url)
    images = [img for img in soup.findAll('img')]
    print (str(len(images)) + " images found.")
    print ('Downloading images to current working directory.')
    image_links = [each.get('src') for each in images]
    for each in image_links:
        try:
            filename = each.strip().split('/')[-1].strip()
            src = urllib.parse.urljoin(url, each)
            print ('Getting: ' + filename)
            response = requests.get(src, stream=True)
            # delay to avoid corrupted previews
            time.sleep(1)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        except:
            print ('An error occured. Continuing.')
    print ('Done.')
    if __name__ == '__main__':
       url = sys.argv[0]
    
get_images('https://mm.taobao.com/self/aiShow.htm?spm=719.7763510.1998643336.2.gRK27F&userId=362438816')