import time
from typing import Counter, List

import numpy as np
import SimpleITK as sitk
from tqdm import tqdm


def analyze_shapes(list_of_files: List) -> np.array:
    """Returns a list of all file shapes
    
    Arguments:
    - list_of_files: a Listof files with the MHD extension.
    
    Returns:
    - numpy array that describes the sizes and their counts"""
    results = []
    for file in list_of_files:
        #print(file)
        data = sitk.ReadImage(file.folder)
        shape = np.reshape(data, -1)
        shape = shape.shape[0]
        #results.append(shape)
        del(data)
    return shape
    return Counter(results)



def analyze_data_distribution(list_of_files: List, bins: int = 100) -> np.array:
    """Performs analysis of the distribution of data.

    Arguments:
    - list_of_files: a List of files with the MHD extension.
    - bins: the number of bins to return in the histogram

    Returns:
    - histogram: a numpy array representing a histogram."""
    histogram: List = []
    #list_of_files = [file.folder for file in list_of_files if file.extension == "mhd"]
    for file in list_of_files:
        data = sitk.ReadImage(file.folder)
        data = np.array(sitk.GetArrayFromImage(data), dtype=np.float32)
        data = np.reshape(data, -1)
        histogram.append(data)
    histogram = np.stack(histogram, axis=0)
    histogram = np.reshape(histogram, -1)
    histogram = np.histogram(histogram, bins=bins)
    return histogram


def find_nans(list_of_files: List) -> Counter:
    """Returns the count and location of NaNs"""
    ...

