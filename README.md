# Visual_Assignment_1
## This is the repository for the first assignment in the portfolio for Visual Analytics

### Description of project 
The code for this project aims to find similar images relative to a given target-image in a folder. 

### Method
This project contains a .py script that loads a target-image and a directory defined as an input from the terminal. 
The histogram for the target-image is firstly calculated and normalized using functions from cv2. After this is done for the given target image, it is done on the remaining images from the user defined directory. The script then compares the histograms and finds the three images that has the smallest distance to the target image, based on the histograms. Lastly the script produces an image file containing the target-image and the top three most similar images, including the calculated distance score for each of the images. Further it produces a .CSV file containing the name of the target-image and the three most similar images, placed in descending order according to their relative similarity to the target-image.

### Usage
In order to reproduce the results I have gotten (and which can be found in the "out" folder), a few steps has to be followed:
1) Install the relevant packages - for this script the only package that is necessary to install before running the script is cv2. This is also mentioned in the script as a comment. 
2) Make sure to place the script in the "src" folder and the data in the "in" folder. The data I used can be accessed from this page: https://www.robots.ox.ac.uk/~vgg/data/flowers/102/ 
3) Run the script from the terminal and remember to pass the required arguments (-ti (target_image) and -dn (directory_name)). 

This will give you the same results as I have gotten in your "out" folder". 

### Results
The results of this project is not the best, since this way of comparing images using histograms is not as precise as using eg. transfer learning. This becomes most clear when looking at the closest images in the out folder that contains images of flowers that are not the same color as the target-image, which is not something we as humans would immediately expect. 
It would be interesting to make a script that performs exactly this comparison-task using transfer-learning, in order to see the results of this. 
