"""
RasterData is a Wrapper for the raster data that the machine learning
algorithms and the preprocessing will be done on.
"""
import numpy as np
from preprocessing import get_normalized_bands, apply_gaussian_blur
import gdal


class RasterData():
    """RasterData class """
    def __init__(self, image_path):
        self.org_image_path = image_path
        self.array = self.get_array_from_raster()
        self.height = self.array.shape[0]
        self.width = self.array.shape[1]
        """Shape tuple of the array data"""
        self.shape = self.array.shape

    def reset_raster_data(self):
        """
        Reinitializes the raster_data to the original till file
        """
        self.array = self.get_array_from_raster()

    def get_current_shape(self):
        """
        Return the current shape of array, difference from the
        shape attribute because shape will return the original shape
        """
        return self.array.shape

    def get_array_from_raster(self, dtype=np.float64):
        """
        Return Numpy array from the raster data
        """
        raster_data = gdal.Open(self.org_image_path)
        data = np.empty((raster_data.RasterYSize,
                         raster_data.RasterXSize, raster_data.RasterCount))

        for i in range(1, raster_data.RasterCount+1):
            band = raster_data.GetRasterBand(i).ReadAsArray()
            data[:, :, i-1] = band
        if dtype == np.float32:
            return np.float32(data)

        return data

    def get_array(self, copy=False):
        """
        Returns numpy array of data
        copy: if true returns a new copy of the data if false returns a
              reference to the data
        """
        if copy:
            return self.array.copy()

        return self.array

    def standard_normalize_array(self, inplace=False, returnable=True):
        """
        Normalizes the array using StandardScalar
        inplace: if true will change the objects data if false will return a
                 new normalized data and keep the object reference original
        """
        new_data = get_normalized_bands(self.array.copy())

        if inplace:
            self.array = new_data
        if returnable:
            return new_data

        return None

    def gaussian_blur_array(self, sigma=1, inplace=False, returnable=True):
        """
        Applies blurring affect on raster data to remove noise.
        Sigma: Stanard deviation of the gaussian kernel
        inplace: if true will change the objects data if false will return a
                 new denoised data and keep the object reference original
        """
        new_data = apply_gaussian_blur(self.array.copy(), sigma)

        if inplace:
            self.array = new_data
        if returnable:
            return new_data

        return None

    def flatten_array(self, inplace=False, returnable=True):
        """
        Returns a flattened data array
        inplace: if true will change the objects data
                 if false will copy and return a flattened array
        """
        if len(self.array.shape) != 3:
            return self.array

        flat_data = np.empty((self.height*self.width, self.n_bands))
        data = self.array
        for i in range(0, self.n_bands):
            flat_band = data[:, :, i].reshape(self.width*self.height)
            flat_data[:, i] = flat_band

        if inplace:
            self.array = flat_data

        if returnable:
            return flat_data

        return None

    def reform_array(self, inplace=False, returnable=True):
        """
        Returns a reshaped data array with original dimension
        returnable: if it returns the reshaped array
        inplace: if true will change the objects data amd return it
                 if false will return a copy without changing the objects data
        """
        if len(self.array.shape) == 3:
            return self.array

        org_data = np.empty((self.height, self.width, self.n_bands))
        data = self.array
        for i in range(0, self.n_bands):
            tmp = data[:, i].reshape(self.height, self.width)
            org_data[:, :, i] = tmp

        if inplace:
            self.array = org_data

        if returnable:
            return org_data

        return None
