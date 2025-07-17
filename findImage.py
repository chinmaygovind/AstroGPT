import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

imageDir = "static/images/"
pagesDir = "static/imagepages/"

async def queryImage(fileName):
    # print(f"DEBUG: queryImage called with filename: {fileName}")
    
    # Check if the query image file exists
    if not os.path.exists(fileName):
        # print(f"DEBUG: ERROR - Query image file does not exist: {fileName}")
        return []
    
    img1 = cv.imread(fileName,cv.IMREAD_GRAYSCALE) # queryImage
    if img1 is None:
        # print(f"DEBUG: ERROR - Could not load query image: {fileName}")
        return []
        
    # print(f"DEBUG: Query image loaded, shape: {img1.shape}")
    allMatches = {}

    # Check if imageDir exists
    if not os.path.exists(imageDir):
        # print(f"DEBUG: ERROR - Image directory does not exist: {imageDir}")
        return []
        
    # print(f"DEBUG: Starting directory scan in {imageDir}")
    directories = os.listdir(imageDir)
    # print(f"DEBUG: Found {len(directories)} directories: {directories}")
    
    # Count total files for progress bar
    total_files = 0
    for directory in directories:
        dir_path = imageDir + directory
        if os.path.isdir(dir_path):
            total_files += len(os.listdir(dir_path))
    
    print(f"Searching through {total_files} images...")
    
    with tqdm(total=total_files, desc="Processing images", unit="img") as pbar:
        for directory in directories:
            # print(f"DEBUG: Processing directory: {directory}")
            dir_path = imageDir + directory
            if not os.path.isdir(dir_path):
                # print(f"DEBUG: Skipping {directory} - not a directory")
                continue
                
            for filename in os.listdir(dir_path):
                pbar.set_description(f"Processing {directory}")
                # print(f"DEBUG: Processing file: {directory}/{filename}")
                #print("Trying " + directory + "/" + filename)
                img2 = cv.imread(imageDir + directory + "/" + filename,cv.IMREAD_GRAYSCALE) # trainImage
                if img2 is None:
                    # print(f"DEBUG: Could not load image: {directory}/{filename}")
                    pbar.update(1)
                    continue
                    
                # Initiate ORB detector
                orb = cv.ORB_create()
                # find the keypoints and descriptors with ORB
                kp1, des1 = orb.detectAndCompute(img1,None)
                kp2, des2 = orb.detectAndCompute(img2,None)
                
                if des1 is None or des2 is None:
                    # print(f"DEBUG: No descriptors found for {directory}/{filename}")
                    pbar.update(1)
                    continue
                    
                # create BFMatcher object
                bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
                # Match descriptors.
                try: 
                    matches = bf.match(des1,des2)
                    # Sort them in the order of their distance.
                    matches = sorted(matches, key = lambda x:x.distance)
                    # Draw first 10 matches.
                    #img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

                    allMatches[filename] = matches[0].distance
                    # print(f"DEBUG: Match found for {directory}/{filename}: {matches[0].distance}")
                except Exception as e:
                    # print(f"DEBUG: Error matching {directory}/{filename}: {e}")
                    pass
                
                pbar.update(1)

    # print(f"DEBUG: Total matches found: {len(allMatches)}")
    sortedMatches = dict(sorted(allMatches.items(), key=lambda item: item[1]))
    result = list(sortedMatches.keys())[:10]
    print(f"Found {len(allMatches)} matches. Top 10 results selected.")
    # print(f"DEBUG: Top 10 matches: {result}")
    return result