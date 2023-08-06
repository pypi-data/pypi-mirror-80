"""Main module."""

import psutil
import time
from datetime import datetime
import subprocess
from random import randint
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, sys, configparser, argparse
import random 
import sqlite3 as lite
import logging
import logging.handlers
import re

def logout(self):
        self.browser.quit
        self.browser.close
    
def __init__ (self,config,headless=False):
    self.path="/home/matt/profiles/"
    self.con = lite.connect('bd.db')
    self.cur = self.con.cursor() 
    self.nextswipe = datetime.now
    self.visited_ids=[]

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        if headless:
            chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--no-sandbox")
        self.browser = webdriver.Chrome(config['system']['chromedriver'], options=chrome_options)
    except:
        message="webdriver failed to init"
        raise
    try:
        self.browser.delete_all_cookies()
        self.browser.set_window_size(1200, 1080)
        sleep(3)
        self.browser.get(config['system']['signinurl'])
        sleep(20)
        s = self.browser.page_source
        pattern = "id=\"password(.*?)\""
        code=re.search(pattern, s).group(1)
        #^^^ code is used for preventing automated form submissions!!
        self.browser.find_element_by_name("email").send_keys(config['user']['username'])
        sleep(4)
        self.browser.find_element_by_name("password").send_keys(config['user']['password'])
        self.browser.find_element_by_name("post").click()
        self.connected=True
    except:
        self.connected=False

    return (message,code)