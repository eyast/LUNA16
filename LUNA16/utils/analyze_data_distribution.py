from collections import namedtuple
from functools import lru_cache
from typing import Counter, List

import numpy as np
import SimpleITK as sitk
import dask.array as da

from .analyze_folders import File


@lru_cache(maxsize=100, typed=True)
def analyze_shapes(list_of_files: List[File]) -> int:
    """Returns a list of the 1st channel of each file

    Arguments:
    - list_of_files: a Listof files with the MHD extension.

    Returns:
    - Integer: Number of "slices" in each CT-scan.
    """
    for file in list_of_files:
        data = sitk.ReadImage(file.folder)
        data = np.array(sitk.GetArrayFromImage(data), dtype=np.float32)
    return data.shape[0]


def analyze_distribution_of_all_files(list_of_files: List[File]) -> np.array:
    """Returns individual images"""

    for file in list_of_files:
        data = sitk.ReadImage(file.folder)
        data = np.array(sitk.GetArrayFromImage(data), dtype=np.float32)
        data = da.from_delayed(data, **(data.shape), dtype=np.float32)
    return data


def analyze_data_distribution(list_of_files: List, bins: int = 100) -> np.array:
    """Performs analysis of the distribution of data.

    Arguments:
    - list_of_files: a List of files with the MHD extension.
    - bins: the number of bins to return in the histogram

    Returns:
    - histogram: a numpy array representing a histogram."""
    histogram: List[File] = []
    #list_of_files = [file.folder for file in list_of_files if file.extension == "mhd"]
    for file in list_of_files:
        data: sitk.Image = sitk.ReadImage(file.folder)
        data: np.array = np.array(
            sitk.GetArrayFromImage(data), dtype=np.float32)
        data: np.array = np.reshape(data, -1)
        histogram.append(data)
    histogram = np.stack(histogram, axis=0)
    histogram = np.reshape(histogram, -1)
    histogram = np.histogram(histogram, bins=bins)
    return histogram


def find_nans(list_of_files: List) -> Counter:
    """Returns the count and location of NaNs"""
    ...
