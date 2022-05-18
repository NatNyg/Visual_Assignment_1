# Visual_Assignment_1
## This is the repository for the first assignment in the portfolio for Visual Analytics

### Description of project 
The code for this project aims to find similar images relative to a given target-image in a folder. 

### Method
This project contains two .py scripts
1) The first one (image_search.py) loads a target-image and a directory defined as an input from the terminal. 
The histogram for the target-image is firstly calculated and normalized using functions from cv2. After this is done for the given target image, it is done on the remaining images from the user defined directory. The script then compares the histograms and finds the three images that has the smallest distance to the target image, based on the histograms. Lastly the script produces an image file containing the target-image and the top three most similar images, including the calculated distance score for each of the images. Further it produces a .CSV file containing the name of the target-image and the three most similar images, placed in descending order according to their relative similarity to the target-image (the name of the images is a part of the path for the image - I didn't have the time to find a better solution for this, but could definelety be improved).

2) The second script (image_search_TL.py) is an optimized version, which uses transfer learning for finding the most similar images instead of calculating the histograms for the images. This script uses the VGG16 model for feature extraction and a k nearest neighbors function to find the three most similar images to a predefined target image. The target image can be alternated, but this most be done directly in the script, as it doesn't take any parameters from the commandline. This could potentially be implemented for future use.  

### Usage
In order to reproduce the results I have gotten (and which can be found in the "out" folder), a few steps has to be followed:
1) Install the relevant packages - relevant packages for both scripts can be found in the "requirements.txt" file. 
2) Make sure to place the script in the "src" folder and the data in the "in" folder. The data I used can be accessed from this page: https://www.robots.ox.ac.uk/~vgg/data/flowers/102/ 
3) Run the script from the terminal and remember to pass the required arguments (-ti (target_image) and -dn (directory_name)) for the image_search script - for the upgraded version you shouldn't pass any arguments when running the script. 
-> Make sure to navigate to the main folder before excecuting the script - then you just have to type the following in the terminal:
"python src/image_search.py -ti {name of the desired target image} -dn {name of the desired directory}" or "python src/image_search_TL.py" depending on which script you want to run. 

This will give you approximately the same results as I have gotten in the "out" folder". 

### Results
The results from the original script "image_search.py" is alright - the images are all yellow as well as the target image, but when comparing to the results from the upgraded script, it becomes clear that the method of comparing images using histograms is not as precise as using transfer learning, as I have done in the upgraded script (this is all based on what I, a human, would expect to be most similar images). 
