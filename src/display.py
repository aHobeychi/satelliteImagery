"""
DISPLAY SATELLITE IMAGERY AND CLASSIFICATION RESULTS
"""

from os import path
import numpy as np
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

THREEBANDS = ['rgb', 'agri', 'bathy', 'swi', 'geo']

BRIGHTNESS = {
    'rgb': 1,
    'agri': 3,
    'geo': 2,
}


def show_image(project, image_type, cropped=True):
    """
    Plots Raster Image using matplotlib
    """
    filepath = project.get_image_paths(image_type, cropped)
    if image_type.lower() in THREEBANDS:
        __show_three_bands(filepath, image_type)
        return

    img = rasterio.open(filepath)
    rasterio.plot.show(img, title=image_type, map='RdYlGn', vmin=-1, vmax=1)


def show_classification(project, clusters, image_type='allbands',
                        cropped=True):
    """
    Plots Classification Result
    """
    filepath = project.get_classification_path(image_type, clusters, cropped)
    img = rasterio.open(filepath)
    rasterio.plot.show(img,
                       title='{} with {} clusters'.format(
                           image_type, clusters))


def __show_three_bands(file_path, image_type):
    """
    Used within the file to help with plotting real color imagery
    """
    src = rasterio.open(file_path)
    data = src.read()
    stack1 = __normalize_array(data[0], image_type)
    stack2 = __normalize_array(data[1], image_type)
    stack3 = __normalize_array(data[2], image_type)
    normed = np.dstack((stack1, stack2, stack3))
    plt.imshow(np.clip(normed, 0, 1))
    plt.show()


def __normalize_array(arr, img_type):
    """Normalized the image array to put them within a 0-1 range"""
    arr_min = np.min(arr).astype('float32')
    arr_max = np.max(arr).astype('float32')
    norm = (BRIGHTNESS[img_type]*(arr.astype('float32')
            - arr_min)/(arr_max + arr_min))

    return norm.clip(min=0)
