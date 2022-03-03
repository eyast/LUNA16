"""Class instance used to perform offline analysis for when I need it.
Saves results to disk, reloads them when needed."""

from .analyze_folders import File, analyze_folder
import pickle

class offline_analysis:
    def __init__(self):
        self.filename = "analysis.py"
        ROOT_FOLDER = "/home/azureuser/cloudfiles/data/LUNA16/extracted"
        all_files = analyze_folder(ROOT_FOLDER)
        all_files = [file for file in all_files if file.extension =="mhd"]
        self.data = self.load_from_disk()

    def load_from_disk(self):
        """Attempts at loading an existing dictionary. Returns an 
        empty one is not found"""
        try:
            return pickle.load(open(self.filename, 'rb'))
        except:
            return {}

    def get_stat(self, stat):
        """Key function - used to retrieve a stat from the dictionary.
        If the stat is not found, the stat is queried first"""
        try:
            return self.data[stat]
        except:
            return self.populate_stat(stat)

    def populate_stat(self, stat):
        

