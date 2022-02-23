import multiprocessing
import os
import zipfile
from multiprocessing.pool import ThreadPool
from typing import List
import logging
import time

import requests

THREAD_MULTIPLIER = 2

root_folder: str = "/data"
folders: List = ["download", "extracted"]

urls: List = [
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

def make_folders() -> None:
    """Creates the necessary folders to host the LUNA files"""
    for folder in folders:
        try:
            if not os.path.exists(os.path.join(root_folder, folder)):
                os.makedirs(os.path.join(root_folder, folder))
            else:
                logging.info(f"{folder} folder already exists.")
        except:
            logging.warning(f"Could not create the {folder} folder.")

def unzip(path_name: str) -> None:
    """Unzips all the files in a ZIP file. Should not be called directly.

    Arguments:
        -path_name: str = the path of a ZIP file
    """
    if path_name[-3:].lower() != "zip":
        #logging.info(f"{path_name} is not a ZIP file, exiting.")
        return
    try:
        with zipfile.ZipFile(path_name) as z:
            target = os.path.join(root_folder, folders[1])
            z.extractall(path=target)
            logging.info(f"{path_name} successfully extracted.")
    except:
        logging.error(f"Could not extract the file {path_name}")

def retrieve_filename(url: str) -> str:
    """Extracts the filename from a URL. Should not be called directly.
    
    Arguments:
        - url: string that represents a full URL.
    Returns:
        - filename: string that represents the name of the file in the URI
    """
    filename: str = url.split("/")[-1]
    filename: str = filename.split("?")[0]
    return filename

def download_file(url: str) -> str:
    """Downloads a single file to a local folder. Should not be called directly.
    Arguments:
    - url: str = the URL of a file to download
    """
    file_name: str = retrieve_filename(url)
    path_name: str = os.path.join(root_folder, folders[0], file_name) 
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path_name, 'wb') as f:
            for data in r.iter_content(chunk_size=8192):
                f.write(data)
    return path_name

def download_and_unzip_file(url: str) -> None:
    """Combines download() and unzip(). Used to enable multiprocessing"""
    path_name = download_file(url)
    unzip(path_name)
    os.remove(path_name)
    return path_name
    
if __name__ =="__main__":
    start = time.time()
    make_folders()
    cpu_count = multiprocessing.cpu_count() * THREAD_MULTIPLIER
    logging.info(f"Found {cpu_count} CPUs.")
    results = ThreadPool(cpu_count).imap_unordered(download_and_unzip_file, urls)
    for r in results:
        print(f"Finished processing {r} - time (in m): {round((time.time() - start ) /60)}")
