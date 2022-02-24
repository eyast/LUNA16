from collections import namedtuple
from functools import lru_cache
from typing import Counter, List

import numpy as np
import SimpleITK as sitk


@lru_cache(maxsize=100, typed=True)
def analyze_shapes(list_of_files: List, type: int) -> int:
    """Returns a list of all file shapes

    Arguments:
    - list_of_files: a Listof files with the MHD extension.

    Returns:
    - TBD
    """
    for file in list_of_files:
        File_analysis = namedtuple(
            "File_analysis",
            ["num_channels", "size", "ch1", "ch2", "ch3"])
        # Read each file
        data = sitk.ReadImage(file.folder)
        data = np.array(sitk.GetArrayFromImage(data), dtype=np.float32)
        # Ensure that all files have the same number of channels
        ops = [len(data.shape), data.size, data.shape[0], data.shape[1],
            data.shape[2]]
    return ops[type]


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
