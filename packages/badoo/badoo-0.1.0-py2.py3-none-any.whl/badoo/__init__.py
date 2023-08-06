
import time
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

__author__ = """Matt Burke"""
__email__ = 'matttsburke@gmail.com'
__version__ = '0.1.0'

nextswipe = datetime.now
visited_ids=[]
connected=False
login_url="https://eu1.badoo.com/en/signin/?f=top"


def login(chromedriver,username,password,headless=False):
    global browser
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        if headless:
            chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(chromedriver, options=chrome_options)
    except:
        return False

    try:
        browser.delete_all_cookies()
        browser.set_window_size(1200, 1080)
        browser.get(login_url)
        sleep(9)
        # s = browser.page_source
        # pattern = "id=\"password(.*?)\""
        # code=re.search(pattern, s).group(1)
        # ^^^ code is used for preventing automated form submissions!!
        browser.find_element_by_name("email").send_keys(username)
        sleep(2)
        browser.find_element_by_name("password").send_keys(password)
        browser.find_element_by_name("post").click()
        sleep(5)
        connected=True
    except:
        connected=False
    return (connected)

def browser_get(url):
    if browser.get(url):
        sleep(10)
        if "That’s all your swipes!" in browser.page_source():
            nextswipe=datetime.now() + timedelta(hours=2)
        if "Meet New People on Badoo, Make Friends, Chat, Flirt" or "Sign in" in browser.page_source():
            return False
        if "Accept all" in browser.page_source():
            print ("cookie confirm required")
        return browser.page_source()

    else:
        return False

def logout():
    browser.quit
    browser.close

def get_more_nearby(pages=3):
    gan_ids=[]
    x = range(pages)
    for n in x:
        ids = get_nearby(n)
        if ids:
            gan_ids.extend(ids)  
    return gan_ids

def get_more_visitors(pages=3):
    gan_ids=[]
    x = range(pages)
    for n in x:
        ids = get_visitors(n)
        if ids:
            gan_ids.extend(ids)  
    return gan_ids

def get_nearby(page=1):
    ids=[]
    browser_get("https://badoo.com/search?page="+str(page))  
    sleep(10)
    elems = browser.find_elements_by_tag_name("figure")

    if not elems:
        return False
    else:
        for elem in elems:
            id=elem.get_attribute("data-user-id")
            ids.append(id)
                 
    return (ids)

def get_visitors(page=1):
        ids=[]
        url="https://badoo.com/visitors?page="+str(page)
        browser_get(url)
        sleep(6)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for a in soup.find_all('a', class_="user-card__link"):
            pattern = r"/profile/(.*?)\?folder"
            id=re.search(pattern, str(a)).group(1)
            ids.append(id)
        return ids

def visit_many(ids,like=False):
    if ids:
        for id in ids:
            visit(id,like)

def visit(id,like=False):
        url="https://badoo.com/search/"
        browser_get(url)
        sleep(6)
        id=str(id)
        url="https://badoo.com/profile/"+id
        browser_get(url)
        sleep(5)
        if like == True:
            try:
                browser.find_element_by_css_selector(".profile-action--color-yes").click()
                browser.find_element_by_css_selector(".js-profile-header-more > .btn").click()
                sleep(7)
                browser.find_element_by_link_text("OK").click()
            except:
                pass
        return browser.page_source

