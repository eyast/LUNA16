"""
Library to download the LUNA16 challenge files.
Author: Eyas Taifour
Date: 23/02/2022

if running as part of a pipeline, call download_data.run()
"""

import argparse
from ctypes import Union
import json
import logging
import os
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from time import time
from typing import List
from zipfile import ZipFile

import requests

THREAD_MULTIPLIER = 2
FOLDERS: List = ["download", "extracted"]
URLS: List = [
    "https://zenodo.org/record/3723295/files/annotations.csv?download=1",
    "https://zenodo.org/record/3723295/files/candidates.csv?download=1",
    "https://zenodo.org/record/3723295/files/candidates_V2.zip?download=1",
    "https://zenodo.org/record/3723295/files/evaluationScript.zip?download=1",
    "https://zenodo.org/record/3723295/files/sampleSubmission.csv?download=1",
    "https://zenodo.org/record/3723295/files/seg-lungs-LUNA16.zip?download=1",
    "https://zenodo.org/record/3723295/files/subset0.zip?download=1",
    "https://zenodo.org/record/3723295/files/subset1.zip?download=1",
    "https://zenodo.org/record/3723295/files/subset2.zip?download=1",
    "https://zenodo.org/record/3723295/files/subset3.zip?download=1",
    "https://zenodo.org/record/3723295/files/subset4.zip?download=1",
    "https://zenodo.org/record/3723295/files/subset5.zip?download=1",
    "https://zenodo.org/record/3723295/files/subset6.zip?download=1",
    "https://zenodo.org/record/4121926/files/subset7.zip?download=1",
    "https://zenodo.org/record/4121926/files/subset8.zip?download=1",
    "https://zenodo.org/record/4121926/files/subset9.zip?download=1"
]


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/domain-result.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

parser = argparse.ArgumentParser(description="Downloads the LUNA16 data \
                    and stores it locally.")
parser.add_argument("--d", action="store_true")#, 
                    #default="/home/azureuser/cloudfiles/data/LUNA16")

args = parser.parse_args()
ROOT_FOLDER = args.d


def _make_1_folder(folder=None) -> None:
    """Tries to create a single folder
    
    Arguments:
    - folder: str = named folder"""
    assert isinstance(folder, str)
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            logging.warning(f"{folder} folder already exists.")
    except:
        logging.warning(f"Could not create {folder}.")


def _check_file_extension(filename: str,
                extension: str) -> bool:
    """Checks whether a File has a specific extension
    
    Arguments:
    - filename: str = name of the file
    - extension: str = the extension to validate
    """
    assert isinstance(filename, str) and isinstance(extension, str)
    assert len(extension) > 0 and len(filename) > 0
    displacement: int = len(extension)
    if filename[-displacement:].lower() == extension.lower():
        return True
    else: return False

def make_folders(root_folder: List[str]=ROOT_FOLDER,
                folder_list: List[str]=FOLDERS) -> None:
    """Creates the necessary FOLDERS to host the LUNA files"""
    _make_1_folder(root_folder)
    for folder in folder_list:
        _make_1_folder(os.path.join(root_folder, folder))


def unzip(path_name: str) -> None:
    """Unzips all the files in a ZIP file. Should not be called directly.

    Arguments:
        -path_name: str = the path of a ZIP file
    """
    if not _check_file_extension(path_name, "zip"):
        return
    try:
        with ZipFile(path_name) as z:
            target = os.path.join(ROOT_FOLDER, FOLDERS[1])
            z.extractall(path=target)
            logging.info(f"{path_name} successfully extracted.")
    except:
        logging.error(f"Could not extract the file {path_name}")


def _retrieve_filename(url: str) -> str:
    """Extracts the filename from a URL. Should not be called directly.

    Arguments:
        - url: string that represents a full URL.
    Returns:
        - filename: string that represents the name of the file in the URI
    """
    filename: str = url.split("/")[-1]
    filename = filename.split("?")[0]
    return filename


def download_file(url: str) -> str:
    """Downloads a single file to a local folder. Should not be called
    directly.

    Arguments:
    - url: str = the URL of a file to download
    """
    file_name: str = _retrieve_filename(url)
    path_name: str = os.path.join(ROOT_FOLDER, FOLDERS[0], file_name)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path_name, 'wb') as f:
            for data in r.iter_content(chunk_size=8192):
                f.write(data)
    return path_name


def download_and_unzip_file(url: str) -> str:
    """Combines download() and unzip(). Used to enable multiprocessing"""
    path_name: str = download_file(url)
    unzip(path_name)
    os.remove(path_name)
    return path_name


def write_folder_location_to_disk() -> None:
    """Writes the value of ROOT_FOLDER to a python dictionary called
    ROOT_FOLDER"""
    root_folder_location = {"ROOT_FOLDER" : ROOT_FOLDER}
    with open('ROOT_FOLDER.py', 'w') as settings_file: 
        settings_file.write(json.dumps(root_folder_location))


def run() -> None:
    """Runs in the main section"""
    ROOT_FOLDER: str = args.d
    start = time()
    make_folders()
    cpu: int = cpu_count() * THREAD_MULTIPLIER
    logging.info(f"Found {cpu} CPUs.")
    results = ThreadPool(cpu).imap_unordered(
        download_and_unzip_file, URLS)
    for r in results:
        logging.info(
            f"Done: {(r.split('/'))[-1]} \t\
                - Time: {round((time() - start ) /60, 2)} m.")
    write_folder_location_to_disk()
    os.removedirs(os.path.join(ROOT_FOLDER, FOLDERS[0]))
                

if __name__ == "__main__":
    run()
    
