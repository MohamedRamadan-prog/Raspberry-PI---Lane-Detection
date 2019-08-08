# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 00:16:31 2018

@author: moham
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def canny(image):
    temp = np.copy(image)
    gray = cv2.cvtColor(temp,cv2.COLOR_RGB2GRAY)
    
    # Define a kernel size for Gaussian smoothing / blurring
    kernel_size = 3 # Must be an odd number (3, 5, 7...)
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
    
    # Define our parameters for Canny and run it
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    
    # Display the image
    #plt.imshow(edges, cmap='Greys_r')
    return edges

def hough(image):
    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 1
    theta = np.pi/180
    threshold = 10
    min_line_length = 10
    max_line_gap = 5
    line_image = np.copy(image)*0 #creating a blank to draw lines on
    masked_edges=canny(image)
    # Run Hough on edge detected image
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)
    
    # Iterate over the output "lines" and draw lines on the blank
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255, 0, 0),5)
    
    # Create a "color" binary image to combine with line image
    #color_edges = np.dstack((masked_edges, masked_edges, masked_edges)) 
    
    # Draw the lines on the edge image
    #combo = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0) 
    #plt.imshow(combo)
    return line_image

def mask(image):
    # This time we are defining a four sided polygon to mask
    imshape = image.shape
    ysize = image.shape[0]
    xsize = image.shape[1]
    mask=np.copy(image)*0
    #colored_image = np.dstack((mask, mask, mask))
    top_right=(570, 350)
    top_left=(400, 350)
    bottom_right=(920,540)
    bottom_left= (90,540)
    vertices = np.array([[bottom_left,top_left,top_right,bottom_right]], dtype=np.int32)
    ignore_mask_color =  (255, 0, 0)
    cv2.fillPoly(mask, vertices,ignore_mask_color)
    masked_edges = cv2.bitwise_and(image, mask)
    return masked_edges


## Main Function
# read the video
frame =  cv2.imread('img.jpg')

#canny_out = cv2.VideoWriter('canny_output.mp4',fourcc, 20.0, (960,540))

    
    
        # get the lines drawn 
        lines= hough(frame)  
        #initiate the region of interest
        roi= mask(frame)
        #join the mask with the lines
        join=cv2.bitwise_and(roi,lines)
        final = cv2.addWeighted(frame, 1, join, 1, 0)
       
        cv2.imshow('OUT',final)
            #cv2.imshow('Canny OUT',join)
            #out.write(final)
            #canny_out.write(join)






