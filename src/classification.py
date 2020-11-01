"""
CLASSIFICATION FILE, USED TO ADD CLUSTERING TO IMAGES
"""

import os
import numpy as np
from raster_data import RasterData
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import numpy
from preprocessing import get_normalized_bands
import gdal


def plot_cost_function(project, image_type='allbands', cropped=True):
    """
    plots the cost function for different numbers of clusters
    """

    image_path = project.get_image_paths(image_type, cropped)
    raster_data = gdal.Open(image_path)
    nbands = raster_data.RasterCount
    data = np.empty((raster_data.RasterXSize*raster_data.RasterYSize, nbands))

    for i in range(1, nbands+1):
        band = raster_data.GetRasterBand(i).ReadAsArray()
        data[:, i-1] = band.flatten()

    kval = range(2, 15)
    cost = [KMeans(n_clusters=k, random_state=1).fit(data).inertia_
            for k in kval]

    plt.plot(kval, cost)
    plt.xticks(kval)
    plt.title('K-means cost across K using {} image'.format
              (image_type))
    plt.xlabel('K')
    plt.ylabel('cost')
    plt.show()


def save_output_result(prediction, project, image_path, output_description, cropped):
    """
    Saves The clustering result to a new image
    """
    tiff_driver = gdal.GetDriverByName('GTiff')
    raster_data = gdal.Open(image_path)
    out_data = prediction.reshape((raster_data.RasterYSize,
                                  raster_data.RasterXSize))

    date = 0
    output_path = ''
    if cropped:
        date = image_path.split(os.sep)[-3]
        output_path = (project.get_classification_folder_path() + date +
                       os.sep + 'cropped' + os.sep + output_description)
                       
    else:
        date = image_path.split(os.sep)[-2]
        output_path = (project.get_classification_folder_path() + date +
                       os.sep + output_description)

    # save the original image with gdal
    output_data = tiff_driver.Create(output_path,
                                     raster_data.RasterXSize,
                                     raster_data.RasterYSize,
                                     1, gdal.GDT_Float32)

    output_data.GetRasterBand(1).WriteArray(out_data)


def kmeans_cluster(project, clusters, image_type='allbands',
                   cropped=True, normalized=True):
    """
    Clusters geotiff image using kmeans
    """

    image_path = project.get_image_paths(image_type, cropped)
    data = RasterData(image_path)

    output_path = ''
    if normalized:
        data.standard_normalize_array(inplace=True)
        data.gaussian_blur_array(2)
        output_path = '{}_normalized_kmeans_{}.tiff'.format(clusters, image_type)
    else:
        output_path = '{}_kmeans_{}.tiff'.format(clusters, image_type)


    km = KMeans(n_clusters=clusters)
    prediction = km.fit_predict(data.flatten_array())
    save_output_result(prediction, project, image_path, output_path, cropped)


def gmm_cluster(project, components, image_type='allbands',
                cropped=True, normalized=True):
    """
    Clusters raster data using Gaussian Mixture Models
    """
    image_path = project.get_image_paths(image_type, cropped)
    tiff_driver = gdal.GetDriverByName('GTiff')
    data = 0
    output_path = ''
    if normalized:
        data = get_normalized_bands(image_path)
        output_path = '{}_normalized_gmm_{}.tiff'.format(components, image_type)
    else:
        data = get_raster_data(image_path)
        output_path = '{}_gmm_{}.tiff'.format(components, image_type)

    gmm = GaussianMixture(n_components = components)
    prediction = gmm.fit_predict(data)

    save_output_result(prediction, project, image_path, output_path, cropped)

 
def dbscan_cluster(project, min_samples=3, eps=100, image_type='allbands',
                   cropped=True, normalized=True):
    """
    Clusters raster data using Dbscan model
    """
    image_path = project.get_image_paths(image_type, cropped)
    tiff_driver = gdal.GetDriverByName('GTiff')
    data = get_raster_data(image_path)

    dbscan = DBSCAN(min_samples= min_samples, eps=100)
    prediction = dbscan.fit_predict(data)

    save_output_result(prediction,  project, image_path,
            '{}_{}_{}_dbscan_{}.tiff'.format(min_points,eps, image_type), cropped)
