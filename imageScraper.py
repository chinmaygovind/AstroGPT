import requests
from bs4 import BeautifulSoup
import urllib.request 
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


DSOS = ['Carina Nebula', 'NGC 1333', 'TW Hya', 'HH 7-11', 'AB Aurigae', 'HD 169142', 'Luhman 16', 'V830 Tau b', 'V 1298 Tau b', 'WASP-18b', 'WASP-39b', 'WASP-43b', 'HR 8799', 'Beta Pictoris', '2M 1207', 'TRAPPIST-1']

for search_term in DSOS:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    service = Service(executable_path='chromedriver.exe')
    browser = webdriver.Chrome(service=service, options=options)

    url = rf'https://www.google.no/search?q={search_term}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&safe=active&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=9000'

    print("Searching " + search_term + "...")
    print("Loading page...")
    browser.get(url)
    time.sleep(1)
    print("Page Loaded...")

    print("Loading images...")
    no_of_pagedowns = 10 # each pagedown is ~17 images
    while no_of_pagedowns:
        browser.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1
    print("Images Loaded...")


    soup = BeautifulSoup(browser.page_source, features="html.parser")
    print("Scraped images...")
    browser.quit()

    thumbnails = []

    for raw_img in soup.find_all('img'):
        link = raw_img.get('src')
        
        if link and link.startswith("https://") and "thumbnail" not in link and "favicon" not in link.lower() and "fonts.gstatic.com" not in link.lower():
            thumbnails.append(link)
            pass

    num = 0
    directory = "images/{object}/".format(object=search_term).replace(" ", "_")
    try: 
        os.makedirs(directory)
    except FileExistsError:
        #continue
        pass
    for image in thumbnails:
        print("Saving " + image + "...")
        path = directory + "{object}_{num}.png".format(object=search_term,num=num)
        num += 1
        urllib.request.urlretrieve(image, path)
    print("Finished " + search_term + "...")