import os
from collections import namedtuple
from typing import List


File = namedtuple('File', ['filename', 'folder', 'extension', 'size'])


def analyze_folder(ROOT_FOLDER: str) -> List[File]:
    """Analyzes the content of a folder recurvisvely.

    Parameters:
    - ROOT_FOLDER: the name of the root folder to analyze.

    Returns:
    - all_files: A list of File namedtuple objects.

    Each file has the following signature:
    File = namedtuple('File', ['filename', 'folder', 'extension', 'size'])
    """
    all_files = []
    for path, dirs, files in os.walk(ROOT_FOLDER):
        for f in files:
            fp = os.path.join(path, f)
            extension = fp.split(".")[-1]
            size = os.path.getsize(fp)
            f = f[:-4]
            individual_file = File(f, fp, extension, size)
            all_files.append(individual_file)
    return all_files

