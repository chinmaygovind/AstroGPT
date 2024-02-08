import requests
from bs4 import BeautifulSoup
import urllib.request 
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#'Carina Nebula', 'NGC 1333', 'TW Hya', 'HH 7-11', 'AB Aurigae', 'HD 169142', 'Luhman 16', 'V830 Tau b', 'V 1298 Tau b', 'WASP-18b', 
DSOS = ['Carina Nebula', 'NGC 1333', 'TW Hya', 'HH 7-11', 'AB Aurigae', 'HD 169142', 'Luhman 16', 'V830 Tau b', 'V 1298 Tau b', 'WASP-18b', 'WASP-39b', 'WASP-43b', 'HR 8799', 'Beta Pictoris', '2M 1207', 'TRAPPIST-1']

for search_term in DSOS:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    service = Service(executable_path='chromedriver.exe')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    browser = webdriver.Chrome(service=service, options=options)

    url = rf'https://www.google.no/search?q={search_term}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&safe=active&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=9000'

    print("Searching " + search_term + "...")
    print("Loading page...")
    browser.get(url)
    time.sleep(1)
    print("Page Loaded...")

    print("Loading images...")
    no_of_pagedowns = 5 # each pagedown is ~17 images
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
            thumbnails.append(raw_img)
            pass

    num = 0
    directory = "static/images/{object}/".format(object=search_term).replace(" ", "_")
    pagedirectory = "static/imagepages/{object}/".format(object=search_term).replace(" ", "_")
    if not os.path.isdir(directory): os.makedirs(directory)
    if not os.path.isdir(pagedirectory): os.makedirs(pagedirectory)
    for image in thumbnails:
        try:
            children = image.parent.parent.parent.find_all("a", recursive=False)
            #Saving Image
            imgpath = directory + search_term + "_{0:03}.png".format(num)
            urllib.request.urlretrieve(image["src"], imgpath)
            print("Downloading image: " + image["src"])
            myHref = None
            for child in children:
                print(child)
                link = child.get("href")
                if link and link.startswith("https://") and "thumbnail" not in link and "favicon" not in link.lower() and "fonts.gstatic.com" not in link.lower():
                    myHref = link
                    break
            if myHref:
                print("Saving " + str(myHref))
                pagepath = pagedirectory + search_term + "_page_{0:03}.html".format(num)
                response = requests.get(myHref)
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Save the content of the webpage to a file
                    with open(pagepath, 'wb+') as output_file:
                        output_file.write(response.content)
                    print(f"Webpage downloaded successfully. Saved as {pagepath}")
                else:
                    print(f"Error: Unable to download webpage. Status code: {response.status_code}")
        except Exception as e:
            print(e)
            print(str(search_term) + "_" + str(num) + " failed")
        num += 1
    print("Finished " + search_term + "...")