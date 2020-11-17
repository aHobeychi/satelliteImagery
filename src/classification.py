"""
CLASSIFICATION FILE, USED TO ADD CLUSTERING TO IMAGES
"""
import os
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
import numpy as np
import matplotlib.pyplot as plt
import gdal
from raster_data import RasterData
from logger import Logger


def plot_cost_function(project, image_type='rgb',
                       cropped=True, normalized=True):
    """
    plots the cost function for different numbers of clusters
    """
    log = Logger()

    image_path, date = project.get_image_paths(image_type,
                                               cropped, get_date=True)
    data = RasterData(image_path)
    if normalized:
        data.standard_normalize_array(inplace=True)

    kval = range(2, 5)
    costs = []
    for k in kval:
        kmeans_model = KMeans(n_clusters=k, random_state=0)
        prediction = kmeans_model.fit_predict(data.flatten_array())

        results = list(np.unique(prediction,return_counts=True)[1])
        list.sort(results)
        costs.append(kmeans_model.inertia_)

        log.log(project.project_name, date, image_type, k, cropped, normalized,
                'kmeans', kmeans_model.inertia_, str(results))
        log.push_information()

    plt.plot(kval, costs)
    plt.xticks(kval)
    plt.title('K-means cost across K using {} image'.format
              (image_type))
    plt.xlabel('K')
    plt.ylabel('cost')
    plt.show()


def save_output_result(prediction, project, image_path,
                       output_description, cropped):
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

    log = Logger()
    image_path, date = project.get_image_paths(image_type,
                                               cropped, get_date=True)
    data = RasterData(image_path)

    output_path = ''
    if normalized:
        data.standard_normalize_array(inplace=True)
        data.gaussian_blur_array(5)
        output_path = '{}_normalized_blurred2_kmeans_{}.tiff'.format(clusters,
                                                            image_type)
    else:
        output_path = '{}_kmeans_{}.tiff'.format(clusters, image_type)

    kmeans_model = KMeans(n_clusters=clusters, n_init=80)
    prediction = kmeans_model.fit_predict(data.flatten_array())

    results = list(np.unique(prediction,return_counts=True)[1])
    list.sort(results)
    log.log(project.project_name, date, image_type, clusters, cropped,
            normalized, 'kmeans', kmeans_model.inertia_, str(results))

    log.push_information()
    save_output_result(prediction, project, image_path, output_path, cropped)


def gmm_cluster(project, components, image_type='allbands',
                cropped=True, normalized=True):
    """
    Clusters raster data using Gaussian Mixture Models
    """
    image_path, date = project.get_image_paths(image_type,
                                               cropped, get_date=True)
    data = RasterData(image_path)
    log = Logger()

    jkkoutput_path = ''
    if normalized:
        data.standard_normalize_array(inplace=True)
        output_path = '{}_normalized_gmm_{}.tiff'.format(components,
                                                         image_type)
    else:
        output_path = '{}_gmm_{}.tiff'.format(components, image_type)

    gmm = GaussianMixture(n_components=components, n_init=10)
    prediction = gmm.fit_predict(data.flatten_array())
    save_output_result(prediction, project, image_path, output_path, cropped)

    results = list(np.unique(prediction,return_counts=True)[1])
    list.sort(results)

    cost = {
            "AIC": gmm.aic(data.flatten_array()),
            "BIC": gmm.bic(data.flatten_array())
    }
    log.log(project.project_name, date, image_type, components, cropped,
            normalized, 'gmm', cost, str(results))
    log.push_information()


def dbscan_cluster(project, min_samples=3, eps=100, image_type='rgb',
                   cropped=True, normalized=True):
    """
    Clusters raster data using Dbscan model
    """
    image_path = project.get_image_paths(image_type, cropped)
    data = RasterData(image_path)

    output_path = ''
    if normalized:
        data.standard_normalize_array(inplace=True)
        data.gaussian_blur_array(2)
        output_path = '{}_normalized_dbscan_{}_{}.tiff'.format(eps, min_samples,
                                                               image_type)
    else:
        output_path = '{}_dbscan_{}_{}.tiff'.format(eps, min_samples,
                                                    image_type)

    dbscan = DBSCAN(min_samples=min_samples, eps=100)
    prediction = dbscan.fit_predict(data.flatten_array())
    save_output_result(prediction, project, image_path, output_path, cropped)
