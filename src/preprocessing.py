"""
Utility to preprocess the raster data before applying
other data driven algorithms.
"""
import numpy as np
import gdal
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import gaussian_filter
from skimage.restoration import denoise_bilateral, estimate_sigma


def get_raster_data(image_path, dtype=np.float32):
    """
    Return raster data as a numpy array
    """
    raster_data = gdal.Open(image_path)
    nbands = raster_data.RasterCount
    data = np.empty((raster_data.RasterXSize*raster_data.RasterYSize, nbands))

    for i in range(1, nbands+1):
        band = raster_data.GetRasterBand(i).ReadAsArray()
        data[:, i-1] = band.flatten()
 
    if (dtype == np.float32):
        return np.float32(data)
    else:
        return np.float64(data)

    data = np.float32(data)


def get_normalized_bands(data, dtype=np.float32):
    """
    Receives tiff image path and return normalized numpy array.
    """
    scaler = StandardScaler()
    for band in range(data.shape[-1]):
        data[:,:,band] = scaler.fit_transform(
                data[:,:,band])

    return data

def apply_gaussian_blur(data, sigma):
    """
    Applies blurring affect on raster data to remove noise.
        Sigma: Stanard deviation of the gaussian kernel
    """
    for band in range(data.shape[-1]):
        data[:,:,band] = gaussian_filter(data[:,:,band], sigma)

    return data


def apply_bilateral_filter(data):
    """
    Applies bilateral filter to numpy array are return flattened array.
    Allows the removal of noise while still keeping the contour.
    """
    sigma_estimation = estimate_sigma(noisy_data, multichannel=True, 
            average_sigmas=True)

    for band in range(data.shape[-1]):
        sigma_estimation = estimate_sigma(band, average_sigmas=True)
        data[:,:,band] = denoise_bilateral(band, sigma_color= sigma_estimation)

    return data
