"""
Firstly import the necessary libraries
"""
import argparse
import os
import sys   
import cv2
import matplotlib.pyplot as plt
import glob
import pandas as pd


def load_target_image(target_image_name, directory_name):
    """ 
This function loads the target image that is given as an input in the terminal
    """
    target_image_n = target_image_name
    target_filepath = os.path.join("..","..","..","CDS-VIS",directory_name,target_image_n)
    target_image = cv2.imread(target_filepath)
    return target_image_n, target_image
     

def compare_histograms(target_image_n, target_image, directory_name):
    """
This function calucates the normalized histogram for the target image and compares to the directories' other images' normalized histograms. The calculated histograms for the other images are then appended into a list for later use. Finally it saves a tuple of the three images that is closest to the target image, based on their histograms. I then use the index for each image to identify their filenames from the list of filenames of all the flowers, in order to prepare for the next function that loads each image. 
    """
    target_image_hist = cv2.calcHist([target_image], 
                        [0,1,2], 
                        None, 
                         [8,8,8],
                         [0,256 , 0,256 , 0,256])

    target_image_hist_norm = cv2.normalize(target_image_hist,target_image_hist, 0,255, cv2.NORM_MINMAX)
     
    hist_comparison = []
 
    filepaths = glob.glob(f"../../../CDS-VIS/{directory_name}/*.jpg")


    for filepath in filepaths:
        if not filepath == target_image_n:
            path = os.path.join(filepath)
            image = cv2.imread(path)
            hist = cv2.calcHist([image], 
                                [0,1,2], 
                                None, 
                                [8,8,8],
                                [0,256 , 0,256 , 0,256])
            hist_norm = cv2.normalize(hist,hist, 0,255, cv2.NORM_MINMAX)
            hist_compare = round(cv2.compareHist(target_image_hist_norm, hist_norm, cv2.HISTCMP_CHISQR))
            hist_comparison.append(hist_compare)
        
    top_three = sorted(zip(hist_comparison,range(len(hist_comparison))))[1:4]
    top_three_indexes = [num[1] for num in top_three]
    top_three_filepaths=[(filepaths[top_three_indexes[0]]),(filepaths[top_three_indexes[1]]),(filepaths[top_three_indexes[2]])]
    return top_three_filepaths, top_three, top_three_indexes


def save_images(top_three_filepaths, target_image, top_three, target_image_n, top_three_indexes):
    """
This function first converts the target image from BGR to RGB, as openCV interprets the colorchannels in different order than matplotlib. Then it loads the top three images as RGB and saves all of the images as subplots in a figure including each images' distance score relative to the targetimage, which is then saved to the out folder. It further saves a .csv file containing one column for the filename of the target image and three columns showing the filenames of the closest images in descending order
    """
    filenames = os.listdir(os.path.join("..","..","..","CDS-VIS","flowers"))
    top_three_filenames = [(filenames[top_three_indexes[0]]),(filenames[top_three_indexes[1]]),(filenames[top_three_indexes[2]])]
    
    
    top_names = [target_image_n,top_three_filenames[0],top_three_filenames[1],top_three_filenames[2]]

    rgb_target = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
    similar_images = [rgb_target]


    for image in top_three_filepaths:
        sim_image = cv2.imread(image)
        rgb_image = cv2.cvtColor(sim_image, cv2.COLOR_BGR2RGB)
        similar_images.append(rgb_image)
        

    f, axarr = plt.subplots(2,2)
    axarr[0,0].imshow(similar_images[0])
    axarr[0,1].imshow(similar_images[1])
    axarr[1,0].imshow(similar_images[2])
    axarr[1,1].imshow(similar_images[3])
    
    axarr[0,0].set_axis_off()
    axarr[0,1].set_axis_off()
    axarr[1,0].set_axis_off()
    axarr[1,1].set_axis_off()
    
    axarr[0,0].set_title(f"Target Image: {top_names[0]}")
    axarr[0,1].set_title(f"{top_names[1]} distance: {top_three[0][0]}")
    axarr[1,0].set_title(f"{top_names[2]} distance: {top_three[1][0]}")
    axarr[1,1].set_title(f"{top_names[3]} distance: {top_three[2][0]}")
    
    
    my_path = "out"
    my_fig = "Similar_images.png"

    f.savefig(os.path.join(my_path, my_fig))
    

    df = pd.DataFrame(top_names, index=['Target_image','First_similar','Second_similar','Third_similar'])

    df_transposed = df.transpose()
    
    my_fig ="Similar_images.csv"
    df_transposed.to_csv(os.path.join(my_path, my_fig),encoding='utf-8', index = False)
    return df_transposed

    

def parse_args():
    """
This function initialises the argparse and defines the command line parameters 
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-ti","--target_image",required=True, help = "Name of the target image")
    ap.add_argument("-dn","--directory_name",required=True, help = "Name of the directory of images to compare")
    args = vars(ap.parse_args())
    return args 
 
    
def main():
    """
The main function defines which functions to run and with which arguments, when the script is run from the terminal. 
    """
    args = parse_args()
    target_image_n, target_image = load_target_image(args["target_image"], args["directory_name"])
    top_three_filenames, top_three, top_three_indexes = compare_histograms(target_image_n, target_image, args["directory_name"])
    df_transposed = save_images(top_three_filenames, target_image, top_three, target_image_n, top_three_indexes)
    
    
    
    
if __name__== "__main__":
    main()
