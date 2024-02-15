import requests
from bs4 import BeautifulSoup
import urllib.request 
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from spire.pdf.common import *
from spire.pdf import *
 
DSOs = ['Carina Nebula', 'NGC 1333', 'TW Hya', 'HH 7-11', 'AB Aurigae', 'HD 169142', 'Luhman 16', 'V830 Tau b', 'V 1298 Tau b', 'WASP-18b', 'WASP-39b', 'WASP-43b', 'HR 8799', 'Beta Pictoris', '2M 1207', 'TRAPPIST-1']
state = 0
while True:
    if state == 0:
        print("DSO List")
        for i in range(0, len(DSOs)):
            print("{num}. {DSO}".format(num=i + 1, DSO = DSOs[i]))
        state = int(input("Choose a DSO to scrape: "))
        print(f"Chose {DSOs[state - 1]}")
    else:
        url = input(f"Enter a link to an article about {DSOs[state - 1]}: ")
        paperDir = f"static/papers/{DSOs[state - 1]}"
        if not os.path.isdir(paperDir): os.makedirs(paperDir)
        paperPath = paperDir + "/temp-{datetime.now()}"
        with open(paperPath, "wb") as f:
            f.write(requests.get(url).content)
        if "pdf" in url:
            doc = PdfDocument()
            doc.LoadFromFile(paperPath)
            title = doc.DocumentInformation.Title
            doc.Close()
            os.rename(paperPath, f"static/papers/{DSOs[state - 1]}/title.pdf")

        


