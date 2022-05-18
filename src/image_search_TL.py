"""
Firstly import the necessary libraries
"""
# base tools
import os

# data analysis
import numpy as np
from numpy.linalg import norm 
from sklearn.neighbors import NearestNeighbors

# tensorflow
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input


# matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
   
def extract_features(img_path, model):
    """
    Extract features from image data using pretrained model (we're gonna use VGG16)
    """
    input_shape = (224, 224, 3)
    img = load_img(img_path, target_size=(input_shape[0], 
                                          input_shape[1]))
    img_array = img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    features = model.predict(preprocessed_img)
    flattened_features = features.flatten()
    normalized_features = flattened_features / norm(features)
    return normalized_features    
    

def compare_images():
    """
This function uses the pretrained model VGG16 to extract features from the images in a user-defined directory. It then find the three most similar images to the target images and saves all four images in one plot to the "out" folder. 
    """
    model = VGG16(include_top = False,
             pooling = "avg",
             input_shape = (224,224,3))
    directory_path = os.path.join("..","..","..","CDS-VIS","flowers")
    filenames = sorted(os.listdir(directory_path))
    feature_list = []
    joined_paths = []
    for file in filenames:
        if not file.endswith(".jpg"):
            pass
        else:
            input_path = os.path.join(directory_path, file)
            joined_paths.append(input_path)
            features = extract_features(input_path, model)
            feature_list.append(features)
    joined_paths = sorted(joined_paths)
    neighbors = NearestNeighbors(n_neighbors=4, 
                                 algorithm = 'brute',
                                 metric='cosine').fit(feature_list)
    distances, indices = neighbors.kneighbors([feature_list[23]])
    idxs = []

    for i in range(1,4):
        idxs.append(indices[0][i])
        
    f, ax = plt.subplots(2,2)
    ax[0,0].imshow(mpimg.imread(joined_paths[23]))
    ax[0,1].imshow(mpimg.imread(joined_paths[idxs[0]]))
    ax[1,0].imshow(mpimg.imread(joined_paths[idxs[1]]))
    ax[1,1].imshow(mpimg.imread(joined_paths[idxs[2]]))
    
    ax[0,0].set_axis_off()
    ax[0,1].set_axis_off()
    ax[1,0].set_axis_off()
    ax[1,1].set_axis_off()
    
    ax[0,0].set_title("Target Image")
    ax[0,1].set_title("Picture 1")
    ax[1,0].set_title("Picture 2")
    ax[1,1].set_title("Picture 3")
    
    my_path = "out"
    my_fig = "Similar_images_TL.png"

    f.savefig(os.path.join(my_path, my_fig))
    return my_fig
    

def main():
    """
The main function defines which functions to run, when the script is run from the terminal. 
    """
    my_fig = compare_images()
    
    
    
    
if __name__== "__main__":
    main()