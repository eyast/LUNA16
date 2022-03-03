import numpy as np
import numpy.typing as npt
import SimpleITK as sitk
import functools

def get_uid(path):
    """Returns a uid from a path"""
    path: str = path[:-4]
    path = path.split("/")
    path = path[-1]
    return path

class MHD:
    """Instantiates to represent a single MHD file

    Parameters:
    - file path.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        self.uid = get_uid(path)


    @functools.cached_property
    def sitk_image(self):
        try:
            self._sitk_image
        except:
            self._sitk_image = sitk.ReadImage(self.path)
        return self._sitk_image

    @functools.cached_property
    def origin(self):
        try:
            self._origin
        except:
            self._origin = self.sitk_image.GetOrigin()
        return self._origin

    @functools.cached_property
    def spacing(self):
        try:
            self._spacing
        except:
            self._spacing = self.sitk_image.GetSpacing()
        return self._spacing

    @functools.cached_property
    def size(self):
        try:
            self._size
        except:
            self._size = self.sitk_image.GetSize()
        return self._size

    
    @functools.cached_property
    def num_channels(self):
        return self.size[2]

    def _get_image_array(self, dtype: str = "float32") -> npt.NDArray:
        """Returns the image as a numpy array - Does not perform any transformation"""
        return np.array(sitk.GetImageFromArray(self.sitk_image), dtype=dtype)


# file = "1.3.6.1.4.1.14519.5.2.1.6279.6001.832260670372728970918746541371.mhd"
# folder = "/home/azureuser/cloudfiles/data/LUNA16/extracted/subset0"
# path = os.path.join(folder, file)

# single_file = MHD(path)
# print(single_file.path, single_file.sitk_image, single_file.origin, single_file.spacing, single_file.size, sep="\n\n")
