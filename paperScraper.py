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
DSOs = DSOs[7:]
paperDir = "static/papers/"
graphDir = "static/graphs/"
for DSO in DSOs:
    print("-------------" + DSO + "-------------")
    dsoDir = paperDir + DSO.replace(" ", "_") + "/"
    dsoGraphDir = graphDir + DSO.replace(" ", "_") + "/"
    if not os.path.isdir(dsoDir): os.makedirs(dsoDir)
    if not os.path.isdir(dsoGraphDir): os.makedirs(dsoGraphDir)
    for paperPath in os.listdir(dsoDir):
        try:
            doc = PdfDocument()
            doc.LoadFromFile(dsoDir + paperPath)
            title = doc.DocumentInformation.Title
            print("Loaded " + title)
            images = []
            num = 0
            # Loop through the pages in the document
            for i in range(doc.Pages.Count):
                page = doc.Pages.get_Item(i)
                print(title + ": Grabbed page #" + str(i))
                # Extract images from a specific page
                for image in page.ExtractImages():
                    images.append(image)
                    graphPath = dsoGraphDir + DSO + "_" + title.replace("&", "_").replace(".", "_").replace(":", "_").replace("/", "_").replace("\\", "_") + "_{0:03}.png".format(num)
                    print("Saving " + graphPath)
                    image.Save(graphPath, ImageFormat.get_Png())
                    num += 1
            print(title + ": " + str(images))
            
            doc.Close()
        except Exception as e:
            print("screwed the pooch: " + str(e))

        


