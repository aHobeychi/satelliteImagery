"""
Utility to preprocess the raster data before applying
other data driven algorithms.
"""
import numpy as np
import gdal
from sklearn.preprocessing import StandardScaler
from scipy.ndimage import gaussian_filter
from skimage.restoration import denoise_bilateral, estimate_sigma

def get_normalized_bands(raster_data, dtype=np.float32):
    """
    Receives tiff image path and return normalized numpy array.
    """
    data = get_raster_data(image_path, dtype)
    scaler = StandardScaler()
    for band in range(data.shape[-1]):
        data[:,band] = scaler.fit_transform(
                data[:,band].reshape(-1, 1)).reshape(-1)
    return data


def apply_gaussian_blur(raster_data, x_shape, y_shape, sigma = 1):
    """
    Applies blurring affect on raster data to remove noise.
        Sigma: Stanard deviation of the gaussian kernel
    """
    return gaussian_filter(raster_data.reshape(y_shape,-1), sigma).flatten()


def apply_bilateral_filter(raster_data, x_shape, y_shape):
    """
    Applies bilateral filter to numpy array are return flattened array.
    Allows the removal of noise while still keeping the contour.
    """
    noisy_data = raster_data.reshape(y_shape, -1)
    sigma_estimation = estimate_sigma(noisy_data, multichannel=True, 
            average_sigmas=True)

    return denoise_bilateral(noisy).flatten()
