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
    'rgb': 8,
    'agri': 3,
    'geo': 2,
}


def convert_to_png(project, image_type, cropped=True, classification=False,
                   clusters=0):

    if not classification:
        filepath = project.getImagePath(image_type, cropped)

        if path.exists(filepath.replace('tiff', 'png')):
            return

        if image_type.lower() in THREEBANDS:
            __convert_three_bands(filepath, image_type)
            return

        src = rasterio.open(filepath)
        data = src.read()
        plt.imshow(data[0], cmap='RdYlGn')
        output = filepath.replace('tiff', 'png')
        plt.axis('off')
        plt.savefig(output, dpi=1000, bbox_inches='tight', pad_inches=0)

    if classification:
        filepath = project.get_classification_path(image_type,
                                                   clusters, cropped)
        output = filepath.replace('tiff', 'png')
        img = rasterio.open(filepath)

        data = img.read()
        plt.imshow(data[0], cmap='RdYlGn')
        plt.axis('off')
        plt.savefig(output, dpi=1000, bbox_inches='tight', pad_inches=0)


def __convert_three_bands(file_path, image_type):
    src = rasterio.open(file_path)
    data = src.read()
    stack1 = __normalize_array(data[0], image_type)
    stack2 = __normalize_array(data[1], image_type)
    stack3 = __normalize_array(data[2], image_type)
    normedd = np.dstack((stack1, stack2, stack3))
    plt.imshow(normedd)
    output = file_path.replace('tiff', 'png')
    plt.axis('off')
    plt.savefig(output, dpi=2000, bbox_inches='tight', pad_inches=0)


def show_image(project, image_type, cropped=True):
    filepath = project.get_image_paths(image_type, cropped)
    if image_type.lower() in THREEBANDS:
        __show_three_bands(filepath, image_type)
        return

    img = rasterio.open(filepath)
    rasterio.plot.show(img, title=image_type, map='RdYlGn', vmin=-1, vmax=1)


def show_classification(project, clusters, image_type='allbands',
                        cropped=True):

    filepath = project.get_classification_path(image_type, clusters, cropped)
    img = rasterio.open(filepath)
    rasterio.plot.show(img,
                       title='{} with {} clusters'.format(
                           image_type, clusters))


def __show_three_bands(file_path, image_type):
    src = rasterio.open(file_path)
    data = src.read()
    stack1 = __normalize_array(data[0], image_type)
    stack2 = __normalize_array(data[1], image_type)
    stack3 = __normalize_array(data[2], image_type)
    normed = np.dstack((stack1, stack2, stack3))
    plt.imshow(normed)
    plt.show()


def __normalize_array(arr, img_type):
    """Normalized the image array to put them within a 0-1 range"""
    arr_min = np.min(arr).astype('float32')
    arr_max = np.max(arr).astype('float32')
    norm = (BRIGHTNESS[img_type]*(arr.astype('float32')
            - arr_min)/(arr_max + arr_min))

    return norm.clip(min=0)
