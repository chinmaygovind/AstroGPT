import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os

imageDir = "static/images/"

async def queryImage(fileName):
    img1 = cv.imread(fileName,cv.IMREAD_GRAYSCALE) # queryImage



    allMatches = {}

    for directory in os.listdir(imageDir):
        #print(fileName + ": Trying " + directory)
        for filename in os.listdir(imageDir + directory):
            #print("Trying " + directory + "/" + filename)
            img2 = cv.imread(imageDir + directory + "/" + filename,cv.IMREAD_GRAYSCALE) # trainImage
            # Initiate ORB detector
            orb = cv.ORB_create()
            # find the keypoints and descriptors with ORB
            kp1, des1 = orb.detectAndCompute(img1,None)
            kp2, des2 = orb.detectAndCompute(img2,None)
            # create BFMatcher object
            bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
            # Match descriptors.
            try: 
                matches = bf.match(des1,des2)
                # Sort them in the order of their distance.
                matches = sorted(matches, key = lambda x:x.distance)
                # Draw first 10 matches.
                img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

                allMatches[filename] = matches[0].distance
            except:
                pass

    sortedMatches = dict(sorted(allMatches.items(), key=lambda item: item[1]))
    return list(sortedMatches.keys())[:10]