"""
DISPLAY SATELLITE IMAGERY AND CLASSIFICATION RESULTS
"""

import os
import numpy as np
import rasterio
from rasterio.plot import show
from raster_data import RasterData
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


def show_classification(project, cropped=True):
    """
    Plots Classification Result
    """
    filepath = project.get_classification_path(cropped)
    title = filepath.split(os.sep)[-1].split('.')[0]
    img = rasterio.open(filepath)
    rasterio.plot.show(img, title=title, cmap="magma")


image_type = 'ndvi'
num_clusters = 3
grid_options = {
        # The format is as follows 1. image type, 2. Cropped
        'plot1': ['rgb', True],
        # plot, type, number of clusters
        'plot2': ['kmeans', image_type, True, num_clusters],
        'plot3': ['gmm', image_type, True, num_clusters]
}


def show_grid_results(project):
    """
    Plots Mutipleplots side by side Typically (1x3), first being rgb, second
    being classification result 1 and third being classification result 2
    """
    date = project.get_possible_dates()
    image_path = project.find_image(date, 'rgb')
    original_image = RasterData(image_path)
    normed = __normalize_array(original_image.array, 'rgb')

    plt.close('all')
    ax1 = plt.subplot(121)
    ax1.imshow(normed)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.set_aspect('equal')
    ax1.margins(0, 0)
    ax1.set_title('{} Image'.format(grid_options['plot1'][0].upper()))

    ax2 = plt.subplot(222)
    ax2.imshow(get_result_plot(project, date, *grid_options['plot2']),
               cmap='inferno')
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax2.set_aspect('equal')
    ax2.margins(0, 0)
    ax2.set_title('{} with {} clusters'.format(
                  grid_options['plot2'][0].upper(), grid_options['plot2'][-1]))

    ax3 = plt.subplot(224)
    ax3.imshow(get_result_plot(project, date, *grid_options['plot3']),
               cmap='inferno')
    ax3.set_title(grid_options['plot3'][0])
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_aspect('equal')
    ax3.margins(0, 0)
    ax3.set_title('{} with {} clusters'.format(
                  grid_options['plot3'][0].upper(), grid_options['plot3'][-1]))

    plt.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=None, hspace=None)

    plt.show()


def get_result_plot(project, date, algorithm, training_set, cropped,
                    n_clusters):
    """
    Returns axes of a plot, for a given clustering result
    """
    path = project.find_classification_path(date, algorithm, training_set,
                                            n_clusters, cropped)
    image = RasterData(path)
    return image.array


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
    arr_min = np.min(arr)
    arr_max = np.max(arr)
    norm = (BRIGHTNESS[img_type]*(arr - arr_min)/(arr_max + arr_min))

    return norm
