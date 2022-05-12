#importing the necessary libraries after installing cv2 in the terminal
import argparse
import os
import sys
sys.path.append(os.path.join("..","..","..","CDS-VIS"))
import cv2
import numpy as np
from utils.imutils import jimshow
from utils.imutils import jimshow_channel
import matplotlib.pyplot as plt
import glob
import pandas as pd

#function to load the target image that is given as an input in the terminal 
def load_target_image(target_image_name, directory_name):
    target_image_n = target_image_name
    #creating the file path for a given target image
    target_filepath = os.path.join("..","..","..","CDS-VIS",directory_name,target_image_n)
    #loading the image
    target_image = cv2.imread(target_filepath)
    return target_image_n, target_image
     
#function to calculate the histogram for the target image and compare to the other images in the directory
def compare_histograms(target_image_n, target_image):
    #create a histogram for the target picture:
    target_image_hist = cv2.calcHist([target_image], 
                         [0,1,2], 
                         None, 
                         [8,8,8],
                         [0,256 , 0,256 , 0,256])
    #using the normalize function in order to normalize the values in the histogram
    target_image_hist_norm = cv2.normalize(target_image_hist,target_image_hist, 0,255, cv2.NORM_MINMAX)
    
    
    #creating an empty list that I can append my histograms for all other flower images onto 
    hist_comparison = []

    #defining and saving the path to the all files in the folder ending on jpg using glob 
    filenames = glob.glob("../../../CDS-VIS/flowers/*.jpg")


    #creating a for-loop to iterate through my filenames, create a path to each image, which I then read in using imread
    #I then calculate the histogram for each image, normalizing it, comparing it to the target image, and finally appending the calculated distance score into our empty list

    for name in filenames:
        if not name == target_image_n:
            path = os.path.join(name)
            image = cv2.imread(path)
            hist = cv2.calcHist([image], 
                                [0,1,2], 
                                None, 
                                [8,8,8],
                                [0,256 , 0,256 , 0,256])
            hist_norm = cv2.normalize(hist,hist, 0,255, cv2.NORM_MINMAX)
            hist_compare = cv2.compareHist(target_image_hist_norm, hist_norm, cv2.HISTCMP_CHISQR)
            hist_comparison.append(hist_compare)
            #creating a tuble that takes the hist_comparison next to the index number of the given image
    top_three = sorted(zip(hist_comparison,range(len(hist_comparison))), reverse=True)[:3]
    #Saving the filenames so I can use them for reading in the images later 
    top_three_indexes = [num[1] for num in top_three]
    top_three_filenames=[(filenames[top_three_indexes[0]]),(filenames[top_three_indexes[1]]),(filenames[top_three_indexes[2]])]
    return top_three_filenames, hist_comparison


def save_images(top_three_filenames, target_image, hist_comparison, target_image_n):
    #I first convert my target image to RGB from BGR, as openCV interprets the colorchannels in different order than matplotlib
#I then create an empty list with my target image, so I can display all four pictures together 
#using a for loop to run through the list of filenames, then reading in the pictures, converting to RGB and appending to the list of images

    rgb_target = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
    similar_images = [rgb_target]


    for image in top_three_filenames:
        sim_image = cv2.imread(image)
        rgb_image = cv2.cvtColor(sim_image, cv2.COLOR_BGR2RGB)
        similar_images.append(rgb_image)
        
    #Using the matplotlib subplots function to plot the pictures together

    f, axarr = plt.subplots(2,2)
    #try this off, to see if it plots without axis:
    plt.axis('off')
    axarr[0,0].imshow(similar_images[0])
    axarr[0,1].imshow(similar_images[1])
    axarr[1,0].imshow(similar_images[2])
    axarr[1,1].imshow(similar_images[3])
    
    axarr[0,0].set_title("Target Image")
    axarr[0,1].set_title(f"Picture 1 distance: {hist_comparison[0]}")
    axarr[1,0].set_title(f"Picture 2 distance: {hist_comparison[1]}")
    axarr[1,1].set_title(f"Picture 3 distance: {hist_comparison[2]}")
    
    #creating a path for my image destination and a filename for the output of the figure - then saving it
    my_path = "/work/cds-visual/Assignments/Assignment_1/out"
    my_fig = "Similar_images.png"

    f.savefig(os.path.join(my_path, my_fig))
    #This provides the full path and not just the image name for the top three similar images - work on a better solution!
    top_names = [target_image_n,top_three_filenames[0],top_three_filenames[1],top_three_filenames[2]]

#save to CSV, with one column for the file name of the target image and three columns showing the filenames of the closest images in descending order
    df = pd.DataFrame(top_names, index=['Target_image','First_similar','Second_similar','Third_similar'])

#Using transpose to flip the dataframe from vertical to horizontal 
    df_transposed = df.transpose()
    #writing the results to a CSV file
    my_fig ="Vis_assignment_output.csv"
    df_transposed.to_csv(os.path.join(my_path, my_fig),encoding='utf-8', index = False)
    return df_transposed

    
  
#using parse_args to define the arguments we want to take from the commandline 

def parse_args():
    #initialise argparse 
    ap = argparse.ArgumentParser()
    #command line parameters
    ap.add_argument("-ti","--target_image",required=True, help = "Name of the target image")
    ap.add_argument("-dn","--directory_name",required=True, help = "Name of the directory of images to compare")
    args = vars(ap.parse_args())
    #return list of arguments
    return args 

#defining a main function that defines which functions to run when called 
    
def main():
    #get arguments 
    args = parse_args()
    target_image_n, target_image = load_target_image(args["target_image"], args["directory_name"])
    top_three_filenames, hist_comparison = compare_histograms(target_image_n, target_image)
    df_transposed = save_images(top_three_filenames, target_image, hist_comparison, target_image_n)
    
    
    
    
if __name__== "__main__":
    main()
