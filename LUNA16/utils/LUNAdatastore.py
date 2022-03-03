
import functools
import os
from collections import namedtuple
import pandas as pd
from torch.utils.data import Dataset
import numpy as np

from .analyze_folders import File, analyze_folder
from .MHD import MHD
import random
import torch


class Point:
    def __init__(self, x, y, z, diameter=None) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.diameter = diameter

    def distance(self, other):
        dist = (self.x - other.x)**2 + (self.y -
                                        other.y)**2 + (self.z - other.z)**2
        if self.diameter:
            dist += self.diameter**2
        if other.diameter:
            dist += other.diameter**2
        dist = dist ** 0.5
        return dist

    def is_neighbor(self, other, dist):
        if self.distance(other) <= dist:
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.z}"


class LUNAdatastore(Dataset):
    """Pytorch Dataset that represents the CT scans"""

    def __init__(self):
        ROOT_FOLDER = "/home/azureuser/cloudfiles/data/LUNA16/extracted"
        all_files = analyze_folder(ROOT_FOLDER)
        all_files = [file for file in all_files if file.extension == "mhd"]
        self.all_mhds = [MHD(file.folder) for file in all_files]
        self.annotations = pd.read_csv(
            os.path.join(ROOT_FOLDER, "evaluationScript/annotations/annotations.csv"))


class LUNAdatastore_position(LUNAdatastore):
    def __init__(self, len=50000, dist=5):
        super().__init__()
        self.len = len
        self.dist = dist
        self.x = [-300, 300]
        self.y = [-300, 300]
        self.z = [-500, 500]
        for i, row in self.annotations.iterrows():
            self.annotations.loc[i, "point"] = Point(
                row["coordX"], row["coordY"], row["coordZ"])

    def __len__(self):
        return self.len


    def __getitem__(self, index):
        random.seed(index)
        result = {}

        # Generates a random point
        x = random.uniform(*self.x)
        y = random.uniform(*self.y)
        z = random.uniform(*self.z)
        data = np.array([x, y, z])
        data = torch.from_numpy(data).float()
        temp_point = Point(x, y, z)
        result["data"] = data

        # Find if it's a nodule or not
        all_points = self.annotations.point
        for point in all_points:
            if temp_point.is_neighbor(point, self.dist):
                label = np.array(1)
            else:
                label = np.array(0)
        label = torch.from_numpy(label).float()
        label = torch.unsqueeze(label, dim=0)
        result["label"] = label
        return result
