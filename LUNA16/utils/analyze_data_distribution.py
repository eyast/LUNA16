from functools import lru_cache
from typing import Counter, List
import numpy.typing as npt

import dask
import dask.array as da
import numpy as np
import SimpleITK as sitk

from .analyze_folders import File

def read_mhd(file: File) -> npt.NDArray:
    """ Reads an MHD file, and returns a numpy array"""
    assert isinstance(file, File)
    assert file.extension == "mhd"
    data: sitk.Image = sitk.ReadImage(file.folder)
    data_array: npt.NDArray = np.array(
        sitk.GetArrayFromImage(data),
        dtype=np.float32)
    return data_array


@lru_cache(maxsize=100, typed=True)
def analyze_shapes(list_of_files: List[File]) -> int:
    """Returns a list of the 1st channel of each file

    Arguments:
    - list_of_files: a Listof files with the MHD extension.

    Returns:
    - Integer: Number of "slices"/channels in each CT-scan File.
    """
    for file in list_of_files:
        assert file.extension == "mhd"
        data = sitk.ReadImage(file.folder)
        data_array: npt.NDArray = np.array(sitk.GetArrayFromImage(data), dtype=np.float32)
    return data_array.shape[0]


def read_ct_as_dask(file: File) -> npt.NDArray:
    """Returns individual CT scan as a numpy array.
    
    Arguments:
    - a single File namedtuple - MHD file
    
    Returns:
    - a numpy array in the shape of C, H, W."""
    assert file.extension == "mhd"
    data: sitk.Image = sitk.ReadImage(file.folder)
    data_array: npt.NDArray = np.array(sitk.GetArrayFromImage(data), dtype=np.float32)
    return data_array


def analyze_data_distribution(list_of_files: List, bins: int = 100) -> npt.NDArray:
    """Performs analysis of the distribution of data.

    Arguments:
    - list_of_files: a List of files with the MHD extension.
    - bins: the number of bins to return in the histogram

    Returns:
    - histogram: a numpy array representing a histogram."""
    histogram: List[npt.NDArray] = []
    for file in list_of_files:
        assert file.extension == "mhd"
        data: sitk.Image = sitk.ReadImage(file.folder)
        data_array: npt.NDArray = np.array(
            sitk.GetArrayFromImage(data), dtype=np.float32)
        data_array = np.reshape(data, -1)
        histogram.append(data_array)
    histogram_array: npt.NDArray = np.stack(histogram, axis=0)
    histogram_array = np.reshape(histogram_array, -1)
    histogram_array = np.histogram(histogram_array, bins=bins)
    return histogram_array


def find_nans(list_of_files: List) -> Counter:
    """Returns the count and location of NaNs"""
    ...
